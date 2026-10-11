-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: examprep_ai
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `chats`
--

DROP TABLE IF EXISTS `chats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chats` (
  `chat_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `title` varchar(255) NOT NULL DEFAULT 'New Chat',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`chat_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `chats_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chats`
--

LOCK TABLES `chats` WRITE;
/*!40000 ALTER TABLE `chats` DISABLE KEYS */;
INSERT INTO `chats` VALUES (5,1,'what is the unit 1?','2026-10-10 11:40:14','2026-10-10 12:33:04'),(6,1,'New Chat','2026-10-10 11:40:18','2026-10-10 11:40:18');
/*!40000 ALTER TABLE `chats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `message_id` int NOT NULL AUTO_INCREMENT,
  `chat_id` int NOT NULL,
  `role` enum('user','assistant') NOT NULL,
  `content` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`message_id`),
  KEY `chat_id` (`chat_id`),
  CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`chat_id`) REFERENCES `chats` (`chat_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (6,5,'user','what is the unit 1?','2026-10-10 11:40:32'),(7,5,'user','what is the unit 1?','2026-10-10 11:41:25'),(8,5,'user','what is the unit 1?','2026-10-10 12:32:55'),(9,5,'assistant','Based on the provided study material, **Unit 1** is titled **Overview of System Software**. \n\nIt covers fundamental concepts, including:\n* Definitions and differences between **system software** and **application software** (with examples).\n* The **software hierarchy** and types of computer languages.\n* **System software tools** and the **life cycle of a source program**.','2026-10-10 12:33:04'),(10,5,'user','whar are the important questions from this pdf','2026-10-10 12:34:32'),(11,5,'assistant','Based on the provided study material, the document itself is a compiled question bank of viva questions categorized into 9 units. The most frequently asked, core questions suitable for 2 marks across these units include:\n\n1. **Definitions & Differences:**\n   * Difference between system software and application software (Unit 1)\n   * Difference between a compiler and an interpreter (Unit 8)\n   * Difference between a token and a lexeme (Unit 6)\n   * Difference between compile time and runtime (Unit 9)\n\n2. **Core Concepts & Components:**\n   * What are one-pass and two-pass assemblers / macro processors? (Units 3 & 4)\n   * What is the purpose of SYMTAB, LITTAB, and POOLTAB? (Unit 3)\n   * What are the main functions of a linker and a loader? (Unit 5)\n   * What are the phases of a compiler and code optimization? (Unit 7)\n   * What is ambiguity in grammar? (Unit 6)','2026-10-10 12:34:40'),(12,5,'user','next unit name','2026-10-10 14:28:41'),(13,5,'user','next unit name','2026-10-10 14:29:32'),(14,5,'user','next unit name','2026-10-10 14:29:38'),(15,5,'user','next unit name','2026-10-10 14:29:41'),(16,5,'assistant','The study material only lists topics up to **Unit 9: Programming Languages**. \n\nThe name of the next unit (such as Unit 10) is **not provided in the study material**.','2026-10-10 14:30:32'),(17,5,'assistant','The name of the next unit is not mentioned in the provided study material, as the material only lists topics up to **Unit 9: Programming Languages**.','2026-10-10 14:31:19'),(18,5,'assistant','The provided study material does not specify which unit you are currently referring to, nor does it list any unit after **Unit 9: Programming Languages**. \n\nTherefore, this information is not available in the provided material.','2026-10-10 14:31:22'),(19,5,'user','what is inside te pdf?','2026-10-10 16:28:27'),(20,5,'assistant','Based on the provided study material, the document **`SS_VIVA Questions.pdf`** contains a curated list of viva/revision questions divided across **9 units** covering the subject of **System Software**. \n\nHere is a summary of the contents inside the PDF:\n\n1. **Unit 1: Overview of System Software**  \n   Contains questions on the definition and examples of system and application software, software hierarchy levels, computer languages, system tools, and program lifecycles.\n\n2. **Unit 2: Overview of Language Processors**  \n   Focuses on language processors (compilers, interpreters, assemblers) and the role and contents of symbol tables.\n\n3. **Unit 3: Assemblers**  \n   Includes questions on types of assemblers (one-pass and two-pass) and assembler tables such as `SYMTAB`, `LITTAB`, and `POOLTAB`.\n\n4. **Unit 4: Macro and Macro Processors**  \n   Covers definitions of macros, core tasks and functions of macro processors, and one-pass vs. two-pass macro processing.\n\n5. **Unit 5: Linkers and Loaders**  \n   Focuses on the need and functions of linkers and loaders, as well as static and dynamic linking.\n\n6. **Unit 6: Scanning and Parsing**  \n   Contains questions on grammar (and ambiguity), lexical analysis (tokens, lexemes, scanners), and tools like `LEX` and `YACC`.\n\n7. **Unit 7: Compilers**  \n   Covers compiler phases and outputs, semantic gap, intermediate code representations (e.g., three-address code, syntax trees), and code optimization techniques.\n\n8. **Unit 8: Interpreters & Debuggers**  \n   Covers how interpreters work, comparisons with compilers, the Java Virtual Machine (JVM), syntax errors, and debuggers.\n\n9. **Unit 9: Programming Languages**  \n   Includes questions about high-level languages, data types and structures, scope of variables, and differences between compile-time and runtime.','2026-10-10 16:29:56');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_results`
--

DROP TABLE IF EXISTS `quiz_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quiz_results` (
  `result_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `subject` varchar(100) DEFAULT NULL,
  `score` int NOT NULL,
  `total` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`result_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `quiz_results_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_results`
--

LOCK TABLES `quiz_results` WRITE;
/*!40000 ALTER TABLE `quiz_results` DISABLE KEYS */;
INSERT INTO `quiz_results` VALUES (1,1,'Data Structure',0,5,'2026-10-10 11:43:21'),(2,1,'Overview of System Software',4,5,'2026-10-10 12:35:31');
/*!40000 ALTER TABLE `quiz_results` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `student_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'ABC','abc@gmail.com','$2b$12$Kv9u2BMtKzuI7ZeCmX4O4OPVgZNLD2NvkexCc.Nxv7v7m4dVxgO92','2026-10-10 10:55:11');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-11 11:29:03
