import streamlit as st
import sqlite3
import bcrypt
import pymupdf
import json
from google import genai

# ---------- APP SETTINGS ----------
st.set_page_config(page_title="ExamPrep AI", page_icon="📚")
st.title("📚 ExamPrep AI")

AI = st.secrets["gemini"]
DB_PATH = "examprep.db"


# ---------- DATABASE (SQLite) ----------
def connect():
    con = sqlite3.connect(DB_PATH, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def init_db():
    con = connect()
    con.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS chats (
            chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            title TEXT NOT NULL DEFAULT 'New Chat',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chat_id) REFERENCES chats(chat_id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS quiz_results (
            result_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
        );
    """)
    con.commit()
    con.close()


def query(sql, values=(), fetch=False):
    con = connect()
    try:
        cur = con.execute(sql, values)
        result = [dict(row) for row in cur.fetchall()] if fetch else None
        con.commit()
        return result
    finally:
        con.close()


init_db()


# ---------- AUTHENTICATION ----------
def register(name, email, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:
        query(
            "INSERT INTO students (name,email,password_hash) VALUES (?,?,?)",
            (name, email, hashed)
        )
        return True
    except sqlite3.IntegrityError:
        return False


def login(email, password):
    users = query(
        "SELECT * FROM students WHERE email=?", (email,), fetch=True
    )
    return users[0] if users and bcrypt.checkpw(
        password.encode(), users[0]["password_hash"].encode()
    ) else None


# ---------- GEMINI AI ----------
def ask_ai(prompt):
    client = genai.Client(api_key=AI["api_key"])
    response = client.models.generate_content(
        model=AI["model"],
        contents=prompt
    )
    return response.text or "Sorry, no answer was generated."


# ---------- CHAT FUNCTIONS ----------
def new_chat(student_id):
    query("INSERT INTO chats (student_id,title) VALUES (?,?)",
          (student_id, "New Chat"))
    rows = query(
        "SELECT chat_id FROM chats WHERE student_id=? "
        "ORDER BY chat_id DESC LIMIT 1",
        (student_id,), fetch=True
    )
    return rows[0]["chat_id"]


def get_chats(student_id):
    return query(
        "SELECT * FROM chats WHERE student_id=? ORDER BY updated_at DESC",
        (student_id,), fetch=True
    )


def get_messages(chat_id, student_id):
    return query(
        """SELECT m.role,m.content FROM messages m
           JOIN chats c ON m.chat_id=c.chat_id
           WHERE c.chat_id=? AND c.student_id=?
           ORDER BY m.message_id""",
        (chat_id, student_id), fetch=True
    )


def save_message(chat_id, role, content):
    query(
        "INSERT INTO messages (chat_id,role,content) VALUES (?,?,?)",
        (chat_id, role, content)
    )
    query("UPDATE chats SET updated_at=CURRENT_TIMESTAMP WHERE chat_id=?", (chat_id,))


def delete_chat(chat_id, student_id):
    query("DELETE FROM chats WHERE chat_id=? AND student_id=?",
          (chat_id, student_id))


# ---------- PDF EXTRACTION ----------
def read_pdfs(files):
    documents = []
    for file in files:
        if file.size > 10 * 1024 * 1024:
            st.warning(f"{file.name} is larger than 10 MB and was skipped.")
            continue
        try:
            with pymupdf.open(stream=file.getvalue(), filetype="pdf") as pdf:
                if len(pdf) > 200:
                    st.warning(f"{file.name} has more than 200 pages and was skipped.")
                    continue
                text = "\n".join(page.get_text() for page in pdf)
                if text.strip():
                    documents.append(f"\n--- {file.name} ---\n{text[:100000]}")
                else:
                    st.warning(
                        f"No selectable text found in {file.name}. "
                        "Scanned PDFs need OCR."
                    )
        except Exception:
            st.warning(f"Could not read {file.name}. Please check the PDF.")
    return documents


# ---------- QUIZ FUNCTIONS ----------
def generate_quiz(subject, context, count):
    prompt = f"""
Create {count} multiple-choice questions for {subject}.
Use this study material:
{context[:30000]}

Return ONLY a JSON array in this format:
[
  {{
    "question": "Question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": 0
  }}
]
The answer is the zero-based index of the correct option.
"""
    text = ask_ai(prompt).strip()
    text = text.removeprefix("```json").removeprefix("```").removesuffix("```")
    questions = json.loads(text)

    if not isinstance(questions, list) or not questions:
        raise ValueError("No questions returned.")

    for q in questions:
        if (not isinstance(q.get("question"), str)
                or not isinstance(q.get("options"), list)
                or len(q["options"]) != 4
                or not isinstance(q.get("answer"), int)
                or isinstance(q["answer"], bool)
                or q["answer"] not in range(4)):
            raise ValueError("Invalid quiz format.")

    return questions


# ---------- LOGIN / REGISTER SCREEN ----------
if "student" not in st.session_state:
    st.session_state.student = None
if "documents" not in st.session_state:
    st.session_state.documents = []
if "active_chat" not in st.session_state:
    st.session_state.active_chat = None
if "quiz" not in st.session_state:
    st.session_state.quiz = None

if not st.session_state.student:
    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email").strip().lower()
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

        if submitted:
            try:
                user = login(email, password)
                if user:
                    st.session_state.student = user
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
            except Exception:
                st.error("Could not connect to the database. Check settings.")

    with register_tab:
        with st.form("register_form"):
            name = st.text_input("Full name")
            email = st.text_input("Email address").strip().lower()
            password = st.text_input("Create password", type="password")
            confirm = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Create account")

        if submitted:
            if not name.strip() or not email or not password:
                st.warning("Please fill in all fields.")
            elif password != confirm:
                st.error("Passwords do not match.")
            elif len(password) < 8:
                st.error("Use a password of at least 8 characters.")
            else:
                try:
                    if register(name.strip(), email, password):
                        st.success("Account created! Please log in.")
                    else:
                        st.error("This email is already registered.")
                except Exception:
                    st.error("Could not create account. Check database settings.")

    st.stop()


# ---------- LOGGED-IN APP ----------
student = st.session_state.student
student_id = student["student_id"]

st.sidebar.success(f"Welcome, {student['name']}!")
page = st.sidebar.radio(
    "Menu", ["Dashboard", "Ask from PDFs", "MCQ Quiz", "Quiz History"]
)

if st.sidebar.button("Logout"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

if page == "Dashboard":
    st.subheader("Your Study Dashboard")
    st.write("Upload your notes, ask questions, and practise MCQs.")
    st.write("Your chats and quiz scores are saved to your account.")

elif page == "Ask from PDFs":
    st.subheader("Ask Questions from Your Study Material")

    uploads = st.file_uploader(
        "Upload PDF notes or question papers",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Load PDFs"):
        if uploads:
            st.session_state.documents = read_pdfs(uploads)
            st.success(f"Loaded {len(st.session_state.documents)} readable PDF(s).")
        else:
            st.warning("Please upload at least one PDF.")

    if st.session_state.documents:
        st.caption(f"{len(st.session_state.documents)} PDF text(s) loaded.")

    chats = get_chats(student_id)

    if st.button("➕ New Chat"):
        st.session_state.active_chat = new_chat(student_id)
        st.rerun()

    if chats:
        labels = {c["chat_id"]: c["title"] for c in chats}
        ids = list(labels)
        current = st.session_state.active_chat
        index = ids.index(current) if current in ids else 0

        chosen = st.selectbox(
            "Saved chats",
            ids,
            index=index,
            format_func=lambda x: labels[x]
        )
        st.session_state.active_chat = chosen

        if st.button("Delete selected chat"):
            delete_chat(chosen, student_id)
            st.session_state.active_chat = None
            st.rerun()

    if not st.session_state.active_chat:
        st.session_state.active_chat = new_chat(student_id)
        st.rerun()

    chat_id = st.session_state.active_chat

    for message in get_messages(chat_id, student_id):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    with st.form("question_form"):
        question = st.text_input("Enter your question")
        marks = st.selectbox("Answer length", [2, 4, 7, 10])
        submit = st.form_submit_button("Get Answer")

    if submit:
        if not question.strip():
            st.warning("Please enter a question.")
        elif not st.session_state.documents:
            st.warning("Upload and load PDFs first.")
        else:
            context = "\n".join(st.session_state.documents)
            prompt = f"""
You are ExamPrep AI, a helpful study assistant.
Answer using the provided study material.
Write an answer suitable for {marks} marks.
Make it clear, accurate, and easy for a student to learn.
If the answer is not in the material, say so.

STUDY MATERIAL:
{context[:50000]}

QUESTION: {question}
"""
            try:
                save_message(chat_id, "user", question)
                answer = ask_ai(prompt)
                save_message(chat_id, "assistant", answer)

                # Give the chat a title based on its first question.
                query(
                    """UPDATE chats SET title=?
                       WHERE chat_id=? AND student_id=?
                       AND title='New Chat'""",
                    (question[:60], chat_id, student_id)
                )
                st.rerun()
            except Exception:
                st.error("AI request failed. Check your Gemini API key and model.")


elif page == "MCQ Quiz":
    st.subheader("Generate an MCQ Quiz")

    subject = st.text_input("Subject or topic")
    count = st.selectbox("Number of questions", [5, 10, 15, 20])

    if st.button("Generate Quiz"):
        if not subject.strip():
            st.warning("Enter a subject or topic.")
        else:
            context = "\n".join(st.session_state.documents)
            try:
                questions = generate_quiz(subject, context, count)
                st.session_state.quiz = {
                    "subject": subject,
                    "questions": questions
                }
            except Exception as e:
                st.error(f"Could not generate quiz: {e}")

    quiz = st.session_state.quiz
    if quiz:
        with st.form("quiz_form"):
            answers = []
            for i, q in enumerate(quiz["questions"]):
                st.markdown(f"**Q{i + 1}. {q['question']}**")
                choice = st.radio(
                    "Choose an answer",
                    range(4),
                    format_func=lambda n, opts=q["options"]: opts[n],
                    key=f"quiz_{i}",
                    index=None
                )
                answers.append(choice)

            submitted = st.form_submit_button("Submit Quiz")

        
        if submitted:
            if any(answer is None for answer in answers):
                st.warning("Please answer every question before submitting.")
            else:
                score = sum(
                    answer == q["answer"]
                    for answer, q in zip(answers, quiz["questions"])
                )
                total = len(quiz["questions"])

            try:
                query(
                    """INSERT INTO quiz_results
                       (student_id,subject,score,total)
                       VALUES (?,?,?,?)""",
                    (student_id, quiz["subject"], score, total)
                )
                st.success(f"Your score: {score}/{total}")
                for i, q in enumerate(quiz["questions"]):
                    st.write(
                        f"Q{i + 1}: Correct answer — "
                        f"{q['options'][q['answer']]}"
                    )
            except Exception as e:
                st.error(f"Score could not be saved: {e}")


elif page == "Quiz History":
    st.subheader("Your Quiz History")
    results = query(
        """SELECT subject,score,total,created_at
           FROM quiz_results WHERE student_id=?
           ORDER BY created_at DESC""",
        (student_id,), fetch=True
    )

    if results:
        st.dataframe(results, use_container_width=True)
    else:
        st.info("No quiz results yet.")