CREATE DATABASE  IF NOT EXISTS `ardeocore` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ardeocore`;
-- MySQL dump 10.13  Distrib 8.0.40, for macos14 (x86_64)
--
-- Host: localhost    Database: ardeocore
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `account_requests`
--
-- Holds user login account request details.
-- The `token` is verified against its expiration time.
-- The associated URL for each request can be used only once.
DROP TABLE IF EXISTS `account_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_date` datetime(6) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `is_url_used` bit(1) DEFAULT NULL,
  `token` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UKkxb7dmieilhvgthkpv8oh1rle` (`token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_requests`
--

LOCK TABLES `account_requests` WRITE;
/*!40000 ALTER TABLE `account_requests` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acl`
--

DROP TABLE IF EXISTS `acl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `acl` (
  `acl_id` int NOT NULL AUTO_INCREMENT,
  `acl_name` varchar(255) NOT NULL,
  `acl_ownername` varchar(255) NOT NULL,
  PRIMARY KEY (`acl_id`),
  UNIQUE KEY `UKc7uc5ptu9m6uatp0goh3o5f3v` (`acl_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acl`
--

LOCK TABLES `acl` WRITE;
/*!40000 ALTER TABLE `acl` DISABLE KEYS */;
/*!40000 ALTER TABLE `acl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `aclentry`
--

DROP TABLE IF EXISTS `aclentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aclentry` (
  `aclentry_id` int NOT NULL AUTO_INCREMENT,
  `aclentry_level` int NOT NULL,
  `acl` int DEFAULT NULL,
  `aclentry_principalId` int DEFAULT NULL,
  `aclentry_aclId` int DEFAULT NULL,
  PRIMARY KEY (`aclentry_id`),
  KEY `FKc685ot2nv6x9ie5pujivq7s9n` (`acl`),
  KEY `FKiy3q404ldtai4y824yhbo4as9` (`aclentry_principalId`),
  KEY `FKsas8pn841u2omhrvisc9o3rol` (`aclentry_aclId`),
  CONSTRAINT `FKc685ot2nv6x9ie5pujivq7s9n` FOREIGN KEY (`acl`) REFERENCES `acl` (`acl_id`),
  CONSTRAINT `FKiy3q404ldtai4y824yhbo4as9` FOREIGN KEY (`aclentry_principalId`) REFERENCES `principal` (`principal_id`),
  CONSTRAINT `FKsas8pn841u2omhrvisc9o3rol` FOREIGN KEY (`aclentry_aclId`) REFERENCES `acl` (`acl_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aclentry`
--

LOCK TABLES `aclentry` WRITE;
/*!40000 ALTER TABLE `aclentry` DISABLE KEYS */;
/*!40000 ALTER TABLE `aclentry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `address`
--

DROP TABLE IF EXISTS `address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `address` (
  `class_type` varchar(31) NOT NULL,
  `address_id` int NOT NULL AUTO_INCREMENT,
  `address_type` varchar(255) NOT NULL,
  `address_value` varchar(255) NOT NULL,
  PRIMARY KEY (`address_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address`
--

LOCK TABLES `address` WRITE;
/*!40000 ALTER TABLE `address` DISABLE KEYS */;
/*!40000 ALTER TABLE `address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `addresses`
--
-- The `addresses` is designed as a base type for multiple address types:
-- `EmailAddress`, `IMAddress`, `PostalAddress`, and `TelephoneNumber`.
-- Intended to be used as `ContactBase` in the `contact_details` table,
-- but this had has not been implemented yet.
DROP TABLE IF EXISTS `addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `addresses` (
  `contact_id` int NOT NULL,
  `address_id` int NOT NULL,
  `child_index` int NOT NULL,
  PRIMARY KEY (`contact_id`,`child_index`),
  KEY `FKq1nxsl09u81nabfbik0ln8xbm` (`address_id`),
  CONSTRAINT `FK9turfjg8628yh0pvfe2a43pr0` FOREIGN KEY (`contact_id`) REFERENCES `contact_base` (`contact_id`),
  CONSTRAINT `FKq1nxsl09u81nabfbik0ln8xbm` FOREIGN KEY (`address_id`) REFERENCES `address` (`address_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses`
--

LOCK TABLES `addresses` WRITE;
/*!40000 ALTER TABLE `addresses` DISABLE KEYS */;
/*!40000 ALTER TABLE `addresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `af_form_data`
--
-- The `af_form_data` table holds form instances (e.g., consultation notes for a patient or subject).
-- Each record is linked to an `episode` (formerly `carespell`), which in turn references a `subject` (formerly `patient`).
-- The structure/design of each form is defined by `af_object`.
-- This table is used in generating Treatment Pathway Metrics.
-- The `xml` column stores user-entered values for the form instance.
-- It contains an XML representation of a `Map<String, FormValue>`.

DROP TABLE IF EXISTS `af_form_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `af_form_data` (
  `af_type` varchar(31) NOT NULL,
  `af_id` int NOT NULL AUTO_INCREMENT,
  `creation_date` datetime(6) DEFAULT NULL,
  `deleted` bit(1) DEFAULT NULL,
  `editable` bit(1) DEFAULT NULL,
  `afo_id` int DEFAULT NULL,
  `guid` varchar(255) NOT NULL,
  `modified_date` datetime(6) DEFAULT NULL,
  `xml` text,
  `episode_id` int DEFAULT NULL,
  `locked` bit(1) DEFAULT NULL,
  `locked_by` varchar(255) DEFAULT NULL,
  `locked_date` datetime(6) DEFAULT NULL,
  `referral_id` int DEFAULT NULL,
  `created_user` int DEFAULT NULL,
  `modified_user` int DEFAULT NULL,
  PRIMARY KEY (`af_id`),
  UNIQUE KEY `UKwusex95xwg5ug0mpl5nnpr77` (`guid`),
  KEY `FKetrxwo7234dse668gmt2vyrx5` (`created_user`),
  KEY `FKdb36p6khh9ip1q4p9abp5rw2w` (`modified_user`),
  CONSTRAINT `FKdb36p6khh9ip1q4p9abp5rw2w` FOREIGN KEY (`modified_user`) REFERENCES `users` (`user_id`),
  CONSTRAINT `FKetrxwo7234dse668gmt2vyrx5` FOREIGN KEY (`created_user`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `af_form_data`
--

LOCK TABLES `af_form_data` WRITE;
/*!40000 ALTER TABLE `af_form_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `af_form_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `af_object`
--
-- The `af_object` table represents a hierarchical structure used to design form pages.
-- It includes various levels: `domain`, `group`, `definition`, `page`, `section`, and `field`.
-- Each `af_form_data` instance is associated with an `af_object` that defines its structure.
-- Pathways are composed of a list of these form designs (`af_object` entries).

DROP TABLE IF EXISTS `af_object`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `af_object` (
  `afo_type` int NOT NULL,
  `afo_id` int NOT NULL AUTO_INCREMENT,
  `afo_h_align` varchar(255) DEFAULT NULL,
  `afo_v_align` varchar(255) DEFAULT NULL,
  `afo_alignment` varchar(255) DEFAULT NULL,
  `afo_bg_colour` varchar(255) DEFAULT NULL,
  `afo_colour_code` varchar(255) DEFAULT NULL,
  `afo_creation_date` datetime(6) DEFAULT NULL,
  `afo_description` varchar(1024) DEFAULT NULL,
  `afo_domain` varchar(255) NOT NULL,
  `field_label_position` varchar(255) DEFAULT NULL,
  `afo_height` int DEFAULT NULL,
  `afo_label` varchar(1024) NOT NULL,
  `afo_label_align` varchar(255) DEFAULT NULL,
  `afo_label_type` varchar(255) DEFAULT NULL,
  `afo_label_url` varchar(255) DEFAULT NULL,
  `afo_modified_date` datetime(6) DEFAULT NULL,
  `afo_name` varchar(255) NOT NULL,
  `roles` varchar(200) DEFAULT NULL,
  `speciality` varchar(255) DEFAULT NULL,
  `afo_unique_string` varchar(255) NOT NULL,
  `afo_width` int DEFAULT NULL,
  `formPage_sectPerRow` int DEFAULT NULL,
  `columns` int DEFAULT NULL,
  `show_title` bit(1) DEFAULT NULL,
  `formDefinition_allow_notes_attachment` bit(1) DEFAULT NULL,
  `formDefinition_allow_notification` bit(1) DEFAULT NULL,
  `formDefinition_Allow_PDF_view` bit(1) DEFAULT NULL,
  `formDefinition_expression` varchar(1000) DEFAULT NULL,
  `formDefinition_liveStatus` int DEFAULT NULL,
  `formDefinition_notifying_users` varchar(255) DEFAULT NULL,
  `formDefinition_owner` varchar(255) DEFAULT NULL,
  `formDefinition_primaryKeyField` varchar(255) DEFAULT NULL,
  `formDefinition_Publish_To_MobilePortal` bit(1) DEFAULT NULL,
  `formDefinition_Publish_To_PatientPortal` bit(1) DEFAULT NULL,
  `formDefinition_show_notes` bit(1) DEFAULT NULL,
  `formField_AssociatedMedia_Link` varchar(255) DEFAULT NULL,
  `formField_bandingDataXmlValue` varchar(2000) DEFAULT NULL,
  `bindExp` varchar(255) DEFAULT NULL,
  `formField_defSequence` varchar(255) DEFAULT NULL,
  `formField_defValMode` int DEFAULT NULL,
  `formField_defValue` varchar(255) DEFAULT NULL,
  `formField_extRefField` varchar(255) DEFAULT NULL,
  `formField_extRef` varchar(255) DEFAULT NULL,
  `formField_fieldType` int DEFAULT NULL,
  `formField_filter_childField` int DEFAULT NULL,
  `formField_filter_HospitalCode` varchar(255) DEFAULT NULL,
  `formField_filter_parentField` int DEFAULT NULL,
  `formField_input_style` varchar(12) DEFAULT NULL,
  `formField_inputType` int DEFAULT NULL,
  `formField_max` varchar(255) DEFAULT NULL,
  `formField_mediaTextBlock` varchar(2000) DEFAULT NULL,
  `formField_min` varchar(255) DEFAULT NULL,
  `formField_mapDomain` varchar(255) DEFAULT NULL,
  `formField_mapName` varchar(255) DEFAULT NULL,
  `formField_pattern` varchar(1000) DEFAULT NULL,
  `formField_referencedField` varchar(255) DEFAULT NULL,
  `formField_required` bit(1) DEFAULT NULL,
  `formField_style` varchar(12) DEFAULT NULL,
  `formField_syncWithReference` bit(1) DEFAULT NULL,
  `afo_parent` int DEFAULT NULL,
  `child_index` int DEFAULT NULL,
  PRIMARY KEY (`afo_id`),
  KEY `FKmoc1etj9csuk0klyp7nx1jc2i` (`afo_parent`),
  CONSTRAINT `FKmoc1etj9csuk0klyp7nx1jc2i` FOREIGN KEY (`afo_parent`) REFERENCES `af_object` (`afo_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `af_object`
--

LOCK TABLES `af_object` WRITE;
/*!40000 ALTER TABLE `af_object` DISABLE KEYS */;
INSERT INTO `af_object` VALUES (0,1,'left','top','horizontal',NULL,NULL,'2025-05-12 17:13:24.009000','Forms root domain','EMDT','left',NULL,'EMDT','left','text',NULL,'2025-05-12 17:13:24.009000','EMDT',NULL,NULL,'/EMDT',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `af_object` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audit_log`
--
-- The `audit_log` table records nearly all user and system actions performed within the application.
-- Logged actions include: login, logout, viewing a patient, referring a patient,
-- adding/viewing/deleting a form instance (`af_form_data`),
-- adding/viewing/deleting form designs (`af_object`),
-- and managing actions on users and patients.

DROP TABLE IF EXISTS `audit_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_log` (
  `audit_id` int NOT NULL AUTO_INCREMENT,
  `audit_date` datetime(6) NOT NULL,
  `audit_form_id` int DEFAULT NULL,
  `audit_module` varchar(255) NOT NULL,
  `audit_result` varchar(255) NOT NULL,
  `audit_user_fullname` varchar(255) DEFAULT NULL,
  `audit_user_username` varchar(255) DEFAULT NULL,
  `audit_action_message` varchar(5000) NOT NULL,
  `subject_id` int DEFAULT NULL,
  `audit_user_id` int DEFAULT NULL,
  PRIMARY KEY (`audit_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_log`
--

LOCK TABLES `audit_log` WRITE;
/*!40000 ALTER TABLE `audit_log` DISABLE KEYS */;
INSERT INTO `audit_log` VALUES (1,'2025-05-12 17:13:24.491000',NULL,'REFERRALS','Starting Server',NULL,NULL,'Server started at 2025/05/12 17:13:23',NULL,NULL);
/*!40000 ALTER TABLE `audit_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `care_provider`
--
-- The `care_provider` table stores additional details related to a user.
-- It typically contains extended information about users in their role as healthcare providers.
DROP TABLE IF EXISTS `care_provider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `care_provider` (
  `id` int NOT NULL AUTO_INCREMENT,
  `address1` varchar(255) DEFAULT NULL,
  `address2` varchar(255) DEFAULT NULL,
  `address3` varchar(255) DEFAULT NULL,
  `allowContactDisplay` bit(1) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `county` varchar(255) DEFAULT NULL,
  `department` varchar(255) DEFAULT NULL,
  `job_title` varchar(255) DEFAULT NULL,
  `mobile_phone` varchar(255) DEFAULT NULL,
  `organisation_name` varchar(255) DEFAULT NULL,
  `personal_information_bio` text,
  `personal_url` varchar(255) DEFAULT NULL,
  `postcode` varchar(255) DEFAULT NULL,
  `preferred_contact` varchar(255) DEFAULT NULL,
  `qualification` varchar(255) DEFAULT NULL,
  `secretary_name` varchar(255) DEFAULT NULL,
  `work_phone` varchar(255) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK4sl72dal85arb8er61h9w5ee4` (`user_id`),
  CONSTRAINT `FK38bakgxat6imwvvod67x5fntf` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `care_provider`
--

LOCK TABLES `care_provider` WRITE;
/*!40000 ALTER TABLE `care_provider` DISABLE KEYS */;
/*!40000 ALTER TABLE `care_provider` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact_base`
--
-- The `contact_base` table was intended to serve as a base for contact-related information,
-- aligning with the design of the `address` hierarchy (`EmailAddress`, `IMAddress`, etc.).
-- However, this table is currently unused in the application.
DROP TABLE IF EXISTS `contact_base`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact_base` (
  `contact_id` int NOT NULL AUTO_INCREMENT,
  `contact_dept` varchar(255) DEFAULT NULL,
  `contact_asstName` varchar(255) DEFAULT NULL,
  `contact_mngrName` varchar(255) DEFAULT NULL,
  `contact_spseName` varchar(255) DEFAULT NULL,
  `contact_office` varchar(255) DEFAULT NULL,
  `contact_org` varchar(255) DEFAULT NULL,
  `contact_profession` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`contact_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_base`
--

LOCK TABLES `contact_base` WRITE;
/*!40000 ALTER TABLE `contact_base` DISABLE KEYS */;
/*!40000 ALTER TABLE `contact_base` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documents`
--
-- The `documents` table holds metadata for all files uploaded within the application.
DROP TABLE IF EXISTS `documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `documents` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category` varchar(255) DEFAULT NULL,
  `comment_guid` varchar(255) DEFAULT NULL,
  `filename` varchar(255) DEFAULT NULL,
  `guid` varchar(255) NOT NULL,
  `note_guid` varchar(255) DEFAULT NULL,
  `original_name` varchar(255) DEFAULT NULL,
  `subject_guid` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `upload_date` datetime(6) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UKlpj6psq23onuyxdu2i9imo2kp` (`guid`),
  KEY `FKkxttj4tp5le2uth212lu49vny` (`user_id`),
  CONSTRAINT `FKkxttj4tp5le2uth212lu49vny` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents`
--

LOCK TABLES `documents` WRITE;
/*!40000 ALTER TABLE `documents` DISABLE KEYS */;
/*!40000 ALTER TABLE `documents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `episode`
--
-- The `episode` table (formerly called `carespell`) represents a unit of care for a subject (or patient).
-- A subject can have multiple episodes, each associated with a different specialty.
-- Each episode can further have multiple associated referrals.
DROP TABLE IF EXISTS `episode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `episode` (
  `episode_id` int NOT NULL AUTO_INCREMENT,
  `guid` varchar(255) NOT NULL,
  `modified_date` datetime(6) NOT NULL,
  `speciality` varchar(255) NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `status` varchar(255) DEFAULT NULL,
  `assistant_id` int DEFAULT NULL,
  `subject_id` int NOT NULL,
  `primary_specialist_id` int DEFAULT NULL,
  `pathway_id` int DEFAULT NULL,
  `item_index` int DEFAULT NULL,
  PRIMARY KEY (`episode_id`),
  UNIQUE KEY `UKgb9p2pt7u15ehvbbcw4arhjqk` (`guid`),
  KEY `FK97ufjnpi0hvguxbnwjooe2t0c` (`assistant_id`),
  KEY `FKqy2dfn396d1i2ghgjjfkwn2hx` (`subject_id`),
  KEY `FKf1ivd42uyhete3clrhcpngtd2` (`primary_specialist_id`),
  KEY `FKhygu5wdfshehfj7ub6kehlq3` (`pathway_id`),
  CONSTRAINT `FK97ufjnpi0hvguxbnwjooe2t0c` FOREIGN KEY (`assistant_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `FKf1ivd42uyhete3clrhcpngtd2` FOREIGN KEY (`primary_specialist_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `FKhygu5wdfshehfj7ub6kehlq3` FOREIGN KEY (`pathway_id`) REFERENCES `pathway` (`pathway_id`),
  CONSTRAINT `FKqy2dfn396d1i2ghgjjfkwn2hx` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`subject_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `episode`
--

LOCK TABLES `episode` WRITE;
/*!40000 ALTER TABLE `episode` DISABLE KEYS */;
/*!40000 ALTER TABLE `episode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `form_sequence`
--
-- In the `af_form_data` table, if the entries are expected to follow a specific sequence.
-- This sequence is used through the form field page.
DROP TABLE IF EXISTS `form_sequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `form_sequence` (
  `id` int NOT NULL AUTO_INCREMENT,
  `current_value` int NOT NULL,
  `format_mask` varchar(255) DEFAULT NULL,
  `increment` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `prefix` varchar(255) DEFAULT NULL,
  `suffix` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UKmielyppaqkuaxa6emy3l8nxl2` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `form_sequence`
--

LOCK TABLES `form_sequence` WRITE;
/*!40000 ALTER TABLE `form_sequence` DISABLE KEYS */;
/*!40000 ALTER TABLE `form_sequence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gp_list`
--
-- used to update patient GPData but not really used
DROP TABLE IF EXISTS `gp_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gp_list` (
  `GPNo` varchar(255) NOT NULL,
  `Health_Centre_or_Road` varchar(255) DEFAULT NULL,
  `Town_or_City` varchar(255) DEFAULT NULL,
  `County` varchar(255) DEFAULT NULL,
  `gpAddress4` varchar(255) DEFAULT NULL,
  `gpEmailAddress` varchar(255) DEFAULT NULL,
  `gpFaxNumber` varchar(255) DEFAULT NULL,
  `Initial` varchar(255) DEFAULT NULL,
  `gpPctCode` varchar(255) DEFAULT NULL,
  `gpPctName` varchar(255) DEFAULT NULL,
  `gpPostcode` varchar(255) DEFAULT NULL,
  `gpPracticeCode` varchar(255) DEFAULT NULL,
  `gpPracticeName` varchar(255) DEFAULT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Phone` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`GPNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gp_list`
--

LOCK TABLES `gp_list` WRITE;
/*!40000 ALTER TABLE `gp_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `gp_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group_usernames`
--
-- used in Acl groups
DROP TABLE IF EXISTS `group_usernames`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `group_usernames` (
  `group_id` int NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  KEY `FKeucndrv32lbsoxjijm2v4uco5` (`group_id`),
  CONSTRAINT `FKeucndrv32lbsoxjijm2v4uco5` FOREIGN KEY (`group_id`) REFERENCES `principal` (`principal_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_usernames`
--

LOCK TABLES `group_usernames` WRITE;
/*!40000 ALTER TABLE `group_usernames` DISABLE KEYS */;
/*!40000 ALTER TABLE `group_usernames` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `identifier_context`
--
-- This table defines identifier contexts.
-- Each identifier context can be associated with multiple organizations.
-- For example, pas1 might be linked to org1 and org2, while pas2 is linked to org3 and org4.
DROP TABLE IF EXISTS `identifier_context`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `identifier_context` (
  `context_id` int NOT NULL AUTO_INCREMENT,
  `guid` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`context_id`),
  UNIQUE KEY `UKhkmssh3rbc9yn1cj6taqf0ssn` (`guid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `identifier_context`
--

LOCK TABLES `identifier_context` WRITE;
/*!40000 ALTER TABLE `identifier_context` DISABLE KEYS */;
/*!40000 ALTER TABLE `identifier_context` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `identifiers`
-- This table stores subject identifiers specific to each identifier context.
-- A subject can have multiple identifiers, one for each identifier context they are part of.
-- For instance, a subject involved with org1 and org2 will have an identifier under pas1,
-- and if also involved with org3 and org4, a separate identifier under pas2.

DROP TABLE IF EXISTS `identifiers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `identifiers` (
  `subject_id` int NOT NULL,
  `identifier` varchar(255) DEFAULT NULL,
  `context_id` int NOT NULL,
  PRIMARY KEY (`subject_id`,`context_id`),
  KEY `FK3u59jaefd9sn9d9s88a5n34kf` (`context_id`),
  CONSTRAINT `FK3u59jaefd9sn9d9s88a5n34kf` FOREIGN KEY (`context_id`) REFERENCES `identifier_context` (`context_id`),
  CONSTRAINT `FKgtpv3q9urr3dy10xuy6tr255b` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`subject_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `identifiers`
--

LOCK TABLES `identifiers` WRITE;
/*!40000 ALTER TABLE `identifiers` DISABLE KEYS */;
/*!40000 ALTER TABLE `identifiers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iep_image_request`
--
-- This table stores metadata for the iep image transfer requests.
DROP TABLE IF EXISTS `iep_image_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `iep_image_request` (
  `iep_img_id` int NOT NULL AUTO_INCREMENT,
  `accession_no` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `direction` varchar(255) DEFAULT NULL,
  `initiating_institution` varchar(255) DEFAULT NULL,
  `last_updated` datetime(6) DEFAULT NULL,
  `priority_name` varchar(255) DEFAULT NULL,
  `responding_institution` varchar(255) DEFAULT NULL,
  `result_code` int DEFAULT NULL,
  `result_message` varchar(255) DEFAULT NULL,
  `send_to_worklist` bit(1) DEFAULT NULL,
  `status_name` varchar(255) DEFAULT NULL,
  `tracking_number` varchar(250) DEFAULT NULL,
  `transaction_date` datetime(6) DEFAULT NULL,
  `transaction_id` varchar(250) DEFAULT NULL,
  `type_name` varchar(255) DEFAULT NULL,
  `vendor_tx_code` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`iep_img_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iep_image_request`
--
-- This table stores log for the iep image transfer requests.
LOCK TABLES `iep_image_request` WRITE;
/*!40000 ALTER TABLE `iep_image_request` DISABLE KEYS */;
/*!40000 ALTER TABLE `iep_image_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `image_transfer_log`
--

DROP TABLE IF EXISTS `image_transfer_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `image_transfer_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `error_desc` varchar(255) DEFAULT NULL,
  `event_date` datetime(6) NOT NULL,
  `event_desc` varchar(255) NOT NULL,
  `accession_number` varchar(255) NOT NULL,
  `note_id` int NOT NULL,
  `subject_id` int NOT NULL,
  `transfer_method` varchar(255) NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image_transfer_log`
--

LOCK TABLES `image_transfer_log` WRITE;
/*!40000 ALTER TABLE `image_transfer_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `image_transfer_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `image_transfer_mapping`
--
-- This table stores an organization's image transfer method used and the one it prefers.
DROP TABLE IF EXISTS `image_transfer_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `image_transfer_mapping` (
  `id` int NOT NULL AUTO_INCREMENT,
  `organisation_id` int NOT NULL,
  `is_preferred` bit(1) DEFAULT NULL,
  `image_transfer_method_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK62b3k61nexg183vagrd3g930e` (`image_transfer_method_id`),
  CONSTRAINT `FK62b3k61nexg183vagrd3g930e` FOREIGN KEY (`image_transfer_method_id`) REFERENCES `image_transfer_method` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image_transfer_mapping`
--

LOCK TABLES `image_transfer_mapping` WRITE;
/*!40000 ALTER TABLE `image_transfer_mapping` DISABLE KEYS */;
/*!40000 ALTER TABLE `image_transfer_mapping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `image_transfer_method`
--
-- This table stores all the image transfer method that's providedd by the application
DROP TABLE IF EXISTS `image_transfer_method`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `image_transfer_method` (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` varchar(100) DEFAULT NULL,
  `image_transfer_interface` varchar(255) DEFAULT NULL,
  `image_transfer_code` varchar(50) NOT NULL,
  `max_hours` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK1xty5j4hllqbq8dynnsyhduo6` (`image_transfer_code`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image_transfer_method`
--

LOCK TABLES `image_transfer_method` WRITE;
/*!40000 ALTER TABLE `image_transfer_method` DISABLE KEYS */;
INSERT INTO `image_transfer_method` VALUES (1,'bbRad automatic transfer','com.ardeo.emdt.imaging.BBRadImagingInterface','bbradauto',2),(2,'DVD sent by post',NULL,'dvd',72),(3,'IEP - Image Exchange Portal','com.ardeo.emdt.imaging.iep.services.IEPImagingService','iep',2);
/*!40000 ALTER TABLE `image_transfer_method` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imaging_status`
--
-- This table stores the status of the subject's image transfer during referrals.
DROP TABLE IF EXISTS `imaging_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `imaging_status` (
  `imaging_status_id` int NOT NULL AUTO_INCREMENT,
  `accession_number` varchar(50) NOT NULL,
  `episode_id` int NOT NULL,
  `current_status` int NOT NULL,
  `last_modified_date` datetime(6) NOT NULL,
  `note_id` int NOT NULL,
  `is_notified` bit(1) NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  `organisation_id` int DEFAULT NULL,
  `image_transfer_method_id` int DEFAULT NULL,
  `subject_id` int NOT NULL,
  PRIMARY KEY (`imaging_status_id`),
  KEY `FK24r8httd8j49w62k06erud8qy` (`organisation_id`),
  KEY `FKeikmhm3yh4juy6induwn3onpv` (`image_transfer_method_id`),
  KEY `FKdxe1k2fkq78cptmqwycl0chch` (`subject_id`),
  CONSTRAINT `FK24r8httd8j49w62k06erud8qy` FOREIGN KEY (`organisation_id`) REFERENCES `organisation` (`id`),
  CONSTRAINT `FKdxe1k2fkq78cptmqwycl0chch` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`subject_id`),
  CONSTRAINT `FKeikmhm3yh4juy6induwn3onpv` FOREIGN KEY (`image_transfer_method_id`) REFERENCES `image_transfer_method` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imaging_status`
--

LOCK TABLES `imaging_status` WRITE;
/*!40000 ALTER TABLE `imaging_status` DISABLE KEYS */;
/*!40000 ALTER TABLE `imaging_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jwt_tokens`
--
-- use for authentication of the costplan api requests
DROP TABLE IF EXISTS `jwt_tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jwt_tokens` (
  `id` int NOT NULL AUTO_INCREMENT,
  `expired` bit(1) NOT NULL,
  `revoked` bit(1) NOT NULL,
  `token` varchar(1000) DEFAULT NULL,
  `tokenType` enum('BEARER') DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FKhy6n4wirmw0ryw2wdmy9cx2mn` (`user_id`),
  CONSTRAINT `FKhy6n4wirmw0ryw2wdmy9cx2mn` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jwt_tokens`
--

LOCK TABLES `jwt_tokens` WRITE;
/*!40000 ALTER TABLE `jwt_tokens` DISABLE KEYS */;
/*!40000 ALTER TABLE `jwt_tokens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu_item`
--
-- the preset menu (system or report) we have in our application is populated from here and can be customized by roles
DROP TABLE IF EXISTS `menu_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_item` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `published` bit(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UKaaw4j0c1b37xh7ntmavh5utpp` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_item`
--

LOCK TABLES `menu_item` WRITE;
/*!40000 ALTER TABLE `menu_item` DISABLE KEYS */;
INSERT INTO `menu_item` VALUES (1,'SYSTEM','About eMDT','ACL_ABOUT_EMDT',_binary '\0'),(2,'SYSTEM','Your User Profile','ACL_YOUR_USER_PROFILE',_binary '\0'),(3,'SYSTEM','Personalise','ACL_PERSONALISE',_binary ''),(4,'SYSTEM','User','ACL_USERS',_binary ''),(5,'SYSTEM','Groups','ACL_GROUPS',_binary ''),(6,'SYSTEM','Roles','ACL_ROLES',_binary ''),(7,'SYSTEM','User Audit Log','ACL_USER_AUDIT_LOG',_binary ''),(8,'SYSTEM','Patient Audit Log','ACL_PATIENT_AUDIT_LOG',_binary ''),(9,'SYSTEM','Form Notifications','ACL_FORM_NOTIFICATIONS',_binary ''),(10,'SYSTEM','User Messaging Preferences','ACL_USER_MESSAGING_PREFERENCES',_binary ''),(11,'SYSTEM','Notifications Schedule','ACL_SET_NOTIFICATIONS_SCHEDULE',_binary '\0'),(12,'SYSTEM','System Messaging','ACL_SYSTEM_MESSAGING',_binary ''),(13,'SYSTEM','Send Test Email','ACL_SEND_TEST_EMAIL',_binary ''),(14,'SYSTEM','Form Editor','ACL_FORM_EDITOR',_binary ''),(15,'SYSTEM','List Editor','ACL_LIST_EDITOR',_binary ''),(16,'SYSTEM','Hospitals','ACL_HOSPITALS',_binary ''),(17,'SYSTEM','Pathways','ACL_PATHWAYS',_binary ''),(18,'SYSTEM','Sequences','ACL_SEQUENCES',_binary ''),(19,'SYSTEM','Inventory','ACL_INVENTORY',_binary ''),(20,'SYSTEM','File Sharing','ACL_FILE_SHARING',_binary ''),(21,'SYSTEM','Login Screen Message','ACL_LOGIN_SCREEN_MESSAGE',_binary ''),(22,'SYSTEM','Import Forms','ACL_IMPORT_FORMS',_binary ''),(23,'SYSTEM','Export Forms','ACL_EXPORT_FORMS',_binary ''),(24,'SYSTEM','Import Users','ACL_IMPORT_USERS',_binary ''),(25,'SYSTEM','Export Users','ACL_EXPORT_USERS',_binary ''),(26,'SYSTEM','Import Patients','ACL_IMPORT_PATIENTS',_binary ''),(27,'SYSTEM','Export Patients','ACL_EXPORT_PATIENTS',_binary ''),(28,'SYSTEM','IEP Setup','ACL_IEP_SETUP',_binary '\0'),(29,'SYSTEM','Import PAS Feeds','ACL_IMPORT_PAS_FEEDS',_binary '\0'),(30,'SYSTEM','Reporting Export','ACL_REPORTING_EXPORT',_binary ''),(31,'SYSTEM','Advanced Settings','ACL_ADVANCED_SETTINGS',_binary ''),(32,'REPORTS','Patient Summaries','ACL_PATIENT_SUMMARIES',_binary ''),(33,'REPORTS','Query Builder','ACL_QUERY_BUILDER',_binary ''),(34,'REPORTS','SQL Queries','ACL_SQL_QUERIES',_binary ''),(35,'REPORTS','Management Reports','ACL_MANAGEMENT_REPORT',_binary ''),(36,'REPORTS','Referrals Detailed Reports','ACL_REFERRALS_DETAILS_REPORT',_binary ''),(37,'REPORTS','Referrals Summary Report','ACL_REFERRALS_SUMMARY_REPORT',_binary ''),(38,'REPORTS','Referrals Users Report','ACL_REFERRALS_USER_STATISTICS',_binary ''),(39,'REPORTS','Notifications Report','ACL_NOTIFICATION_REFERRALS_REPORT',_binary ''),(40,'REPORTS','Meeting Tracking Report','ACL_PATIENT_MEETING_TRACKING_REPORT',_binary ''),(41,'REPORTS','Managed MDM Submissions Report','ACL_NMDM_SUBMISSIONS_REPORT',_binary ''),(42,'REPORTS','Comments Report','ACL_COMMENTS_REPORT',_binary ''),(43,'SYSTEM','Patient Reconciliation','ACL_PATIENT_RECONCILIATION',_binary ''),(44,'SYSTEM','User Reconciliation','ACL_USER_RECONCILIATION',_binary ''),(45,'SYSTEM','Import Events','ACL_IMPORT_EVENTS',_binary ''),(46,'REPORTS','Meeting Attendance Report','ACL_MEETING_ATTENDANCE_REPORT',_binary ''),(47,'SYSTEM','Patient Imaging','ACL_PATIENT_IMAGING',_binary ''),(48,'SYSTEM','PACS Administration','ACL_PACS_ADMIN',_binary ''),(49,'SYSTEM','PAS Administration','ACL_PAS_ADMIN',_binary '');
/*!40000 ALTER TABLE `menu_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `named_list`
--
-- each named_list will have a list of  pairs (key value ) which is used accross the application
DROP TABLE IF EXISTS `named_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `named_list` (
  `nl_id` int NOT NULL AUTO_INCREMENT,
  `nl_creationDate` datetime(6) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `nl_domain` varchar(255) NOT NULL,
  `nl_modifiedDate` datetime(6) DEFAULT NULL,
  `nl_name` varchar(255) NOT NULL,
  `created_by_user` int DEFAULT NULL,
  `modified_by_user` int DEFAULT NULL,
  PRIMARY KEY (`nl_id`),
  UNIQUE KEY `UKe0hverq61dx0k7ypjgi54xm60` (`nl_name`,`nl_domain`),
  KEY `FKwh8om22mwubeifoi8plt2txp` (`created_by_user`),
  KEY `FK22bltbkdbyrdf5ntdt46wwhv8` (`modified_by_user`),
  CONSTRAINT `FK22bltbkdbyrdf5ntdt46wwhv8` FOREIGN KEY (`modified_by_user`) REFERENCES `users` (`user_id`),
  CONSTRAINT `FKwh8om22mwubeifoi8plt2txp` FOREIGN KEY (`created_by_user`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `named_list`
--

LOCK TABLES `named_list` WRITE;
/*!40000 ALTER TABLE `named_list` DISABLE KEYS */;
INSERT INTO `named_list` VALUES (1,'2025-05-12 17:13:24.051000',NULL,'EMDT','2025-05-12 17:13:24.051000','Ethnicity',NULL,NULL),(2,'2025-05-12 17:13:24.053000',NULL,'EMDT','2025-05-12 17:13:24.053000','KeyWorker',NULL,NULL),(3,'2025-05-12 17:13:24.053000',NULL,'EMDT','2025-05-12 17:13:24.053000','Language',NULL,NULL),(4,'2025-05-12 17:13:24.053000',NULL,'EMDT','2025-05-12 17:13:24.053000','Nationality',NULL,NULL),(5,'2025-05-12 17:13:24.053000',NULL,'EMDT','2025-05-12 17:13:24.053000','MaritalStatus',NULL,NULL),(6,'2025-05-12 17:13:24.053000',NULL,'EMDT','2025-05-12 17:13:24.053000','MeetingItemType',NULL,NULL),(7,'2025-05-12 17:13:24.053000',NULL,'EMDT','2025-05-12 17:13:24.053000','PrimarySite',NULL,NULL),(8,'2025-05-12 17:13:24.054000',NULL,'EMDT','2025-05-12 17:13:24.054000','Religion',NULL,NULL),(9,'2025-05-12 17:13:24.055000',NULL,'EMDT','2025-05-12 17:13:24.055000','SexCode',NULL,NULL),(10,'2025-05-12 17:13:24.055000',NULL,'EMDT','2025-05-12 17:13:24.055000','DocumentCategory',NULL,NULL),(11,'2025-05-12 17:13:24.055000',NULL,'EMDT','2025-05-12 17:13:24.055000','Yes_Checkbox',NULL,NULL),(12,'2025-05-12 17:13:24.055000',NULL,'EMDT','2025-05-12 17:13:24.055000','YesNo',NULL,NULL),(13,'2025-05-12 17:13:24.055000',NULL,'EMDT','2025-05-12 17:13:24.055000','YesNoLeftRight',NULL,NULL),(14,'2025-05-12 17:13:24.055000',NULL,'EMDT','2025-05-12 17:13:24.055000','YesNoOther',NULL,NULL),(15,'2025-05-12 17:13:24.055000',NULL,'EMDT','2025-05-12 17:13:24.055000','YesNoRL',NULL,NULL),(16,'2025-05-12 17:13:24.055000',NULL,'EMDT','2025-05-12 17:13:24.055000','YesNoSus',NULL,NULL),(17,'2025-05-12 17:13:24.056000',NULL,'EMDT','2025-05-12 17:13:24.056000','YesNoun',NULL,NULL),(18,'2025-05-12 17:13:24.056000',NULL,'EMDT','2025-05-12 17:13:24.056000','tumourGroup',NULL,NULL),(19,'2025-05-12 17:13:24.056000',NULL,'EMDT','2025-05-12 17:13:24.056000','PatientNOKRelationship',NULL,NULL),(20,'2025-05-12 17:13:24.056000',NULL,'EMDT','2025-05-12 17:13:24.056000','Speciality',NULL,NULL),(21,'2025-05-12 17:13:24.056000',NULL,'EMDT','2025-05-12 17:13:24.056000','Modality',NULL,NULL),(22,'2020-02-14 14:24:07.033000',NULL,'EMDT','2020-02-14 14:24:07.033000','PatientPriority',NULL,NULL),(23,'2025-05-12 17:13:24.064000',NULL,'webapp','2025-05-12 17:13:24.064000','userPrefix',NULL,NULL),(24,'2025-05-12 17:13:24.064000',NULL,'webapp','2025-05-12 17:13:24.064000','userSuffix',NULL,NULL),(25,'2025-05-12 17:13:24.065000',NULL,'EMDT','2025-05-12 17:13:24.065000','ReferringSpecialistJobTitle',NULL,NULL);
/*!40000 ALTER TABLE `named_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organisation`
--
-- a user will belong to an organisation and arganisation can have many subjects and subjects can be refered from one organisation to another
DROP TABLE IF EXISTS `organisation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organisation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `address` varchar(500) DEFAULT NULL,
  `is_central_hub` bit(1) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `creation_date` datetime(6) NOT NULL,
  `code` varchar(250) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `name` varchar(250) DEFAULT NULL,
  `modified_date` datetime(6) NOT NULL,
  `postcode` varchar(100) DEFAULT NULL,
  `hosts_virtual_mdm` bit(1) DEFAULT NULL,
  `context_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UKm2atcosi5hpd5jd2b87cafw2q` (`code`),
  KEY `FK36jajgs0wyf0ho6fxshvnrgln` (`context_id`),
  CONSTRAINT `FK36jajgs0wyf0ho6fxshvnrgln` FOREIGN KEY (`context_id`) REFERENCES `identifier_context` (`context_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organisation`
--

LOCK TABLES `organisation` WRITE;
/*!40000 ALTER TABLE `organisation` DISABLE KEYS */;
/*!40000 ALTER TABLE `organisation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organisation_pathways`
--
-- A pathway can be used by many organisation with the set of their users
DROP TABLE IF EXISTS `organisation_pathways`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organisation_pathways` (
  `id` int NOT NULL AUTO_INCREMENT,
  `guid` varchar(255) NOT NULL,
  `is_published` bit(1) DEFAULT NULL,
  `organisation_id` int DEFAULT NULL,
  `pathway_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK1cjxjj78bbr2o8nes0qlvxfcj` (`guid`),
  KEY `FKjktvdy8moke7t0v95vpqpgo61` (`organisation_id`),
  KEY `FKks5uagb1f99xws4rupf5pxf54` (`pathway_id`),
  CONSTRAINT `FKjktvdy8moke7t0v95vpqpgo61` FOREIGN KEY (`organisation_id`) REFERENCES `organisation` (`id`),
  CONSTRAINT `FKks5uagb1f99xws4rupf5pxf54` FOREIGN KEY (`pathway_id`) REFERENCES `pathway` (`pathway_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organisation_pathways`
--

LOCK TABLES `organisation_pathways` WRITE;
/*!40000 ALTER TABLE `organisation_pathways` DISABLE KEYS */;
/*!40000 ALTER TABLE `organisation_pathways` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `otp_info`
--
-- used for 2FA login via otp
DROP TABLE IF EXISTS `otp_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `otp_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created_date` datetime(6) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `is_used` bit(1) DEFAULT NULL,
  `otp` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `otp_info`
--

LOCK TABLES `otp_info` WRITE;
/*!40000 ALTER TABLE `otp_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `otp_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pacs`
--
-- holds details to connect to dicom
DROP TABLE IF EXISTS `pacs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pacs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `aet` varchar(512) DEFAULT NULL,
  `description` varchar(512) DEFAULT NULL,
  `enabled` bit(1) DEFAULT NULL,
  `ip` varchar(512) DEFAULT NULL,
  `name` varchar(512) DEFAULT NULL,
  `port` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pacs`
--

LOCK TABLES `pacs` WRITE;
/*!40000 ALTER TABLE `pacs` DISABLE KEYS */;
/*!40000 ALTER TABLE `pacs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pacs_organisation`
-- identifier context and organization mapping

DROP TABLE IF EXISTS `pacs_organisation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pacs_organisation` (
  `pacs_id` int NOT NULL,
  `organisation_id` int NOT NULL,
  PRIMARY KEY (`pacs_id`,`organisation_id`),
  KEY `FKp22eprw6xv8t4p0753c17ujci` (`organisation_id`),
  CONSTRAINT `FKp22eprw6xv8t4p0753c17ujci` FOREIGN KEY (`organisation_id`) REFERENCES `organisation` (`id`),
  CONSTRAINT `FKtc88cyqx1vhiydvhy6etxwsqw` FOREIGN KEY (`pacs_id`) REFERENCES `pacs` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pacs_organisation`
--

LOCK TABLES `pacs_organisation` WRITE;
/*!40000 ALTER TABLE `pacs_organisation` DISABLE KEYS */;
/*!40000 ALTER TABLE `pacs_organisation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pair`
-- key value pair listed in named list
DROP TABLE IF EXISTS `pair`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pair` (
  `pair_id` int NOT NULL AUTO_INCREMENT,
  `nl_filter_org_code` varchar(20) DEFAULT NULL,
  `pair_first` varchar(255) NOT NULL,
  `pair_second` varchar(255) NOT NULL,
  `namedList_id` int DEFAULT NULL,
  `child_index` int DEFAULT NULL,
  PRIMARY KEY (`pair_id`),
  KEY `FKdwk10wqjyjufati71ejcvx2ia` (`namedList_id`),
  CONSTRAINT `FKdwk10wqjyjufati71ejcvx2ia` FOREIGN KEY (`namedList_id`) REFERENCES `named_list` (`nl_id`)
) ENGINE=InnoDB AUTO_INCREMENT=224 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pair`
--

LOCK TABLES `pair` WRITE;
/*!40000 ALTER TABLE `pair` DISABLE KEYS */;
INSERT INTO `pair` VALUES (1,'','A','White - British',1,0),(2,'','B','White - Irish',1,1),(3,'','C','White - Any other White background',1,2),(4,'','D','Mixed - White and Black Caribbean',1,3),(5,'','E','Mixed - White and Black African',1,4),(6,'','F','Mixed - White and Asian',1,5),(7,'','G','Mixed - Any other mixed background',1,6),(8,'','H','Asian or Asian British - Indian',1,7),(9,'','J','Asian or Asian British - Pakistani',1,8),(10,'','K','Asian or Asian British - Bangladeshi',1,9),(11,'','L','Asian or Asian British - Other',1,10),(12,'','M','Black or Black British - Caribbean',1,11),(13,'','N','Black or Black British - African',1,12),(14,'','P','Black or Black British - Other',1,13),(15,'','R','Chinese',1,14),(16,'','S','Any other ethnic group',1,15),(17,'','Z','Not Stated',1,16),(18,'','Example Keyworker','Example Keyworker',2,0),(19,'','English','English',3,0),(20,'','French','French',3,1),(21,'','German','German',3,2),(22,'','Italian','Italian',3,3),(23,'','Spanish','Spanish',3,4),(24,'','Dutch','Dutch',3,5),(25,'','Hindi','Hindi',3,6),(26,'','Urdu','Urdu',3,7),(27,'','Punjabi','Punjabi',3,8),(28,'','Asian','Asian',4,0),(29,'','British','British',4,1),(30,'','Irish','Irish',4,2),(31,'','Scottish','Scottish',4,3),(32,'','French','French',4,4),(33,'','German','German',4,5),(34,'','Italian','Italian',4,6),(35,'','Married','Married',5,0),(36,'','Divorced','Divorced',5,1),(37,'','Single','Single',5,2),(38,'','Partner','Partner',5,3),(39,'','Widowed','Widowed',5,4),(40,'','new','New',6,0),(41,'','histology','Histology',6,1),(42,'','radiology','Radiology',6,2),(43,'','oncology','Oncology',6,3),(44,'','surgicalplan','Surgical Plan',6,4),(45,'','discussion','Discussion',6,5),(46,'','followup','Follow Up',6,6),(47,'','HPB','Hepatobilliary',7,0),(48,'','BRN','Brain / Central Nervous System',7,1),(49,'','BRS','Breast',7,2),(50,'','GYN','Gynaecological',7,3),(51,'','HAE','Haematological',7,4),(52,'','HNK','Head and Neck',7,5),(53,'','LGI','Lower Gastro-Intestinal',7,6),(54,'','LUN','Lung',7,7),(55,'','OTH','Other tumour group',7,8),(56,'','SAR','Sarcoma',7,9),(57,'','SKN','Skin',7,10),(58,'','TST','Testicular',7,11),(59,'','UGI','Upper Gastro-Intestinal',7,12),(60,'','URO','Urological',7,13),(61,'','REC','Recovery',7,14),(62,'','NSE','** Not Set **',7,15),(63,'','none','none',8,0),(64,'','Atheist','Atheist',8,1),(65,'','Bahai','Bahai',8,2),(66,'','Baptist','Baptist',8,3),(67,'','Bhuddist','Bhuddist',8,4),(68,'','Born Again Christian','Born Again Christian',8,5),(69,'','Brethren','Brethren',8,6),(70,'','Buddhist','Buddhist',8,7),(71,'','C of E Anglican C of I C of W','C of E Anglican C of I C of W',8,8),(72,'','Christadelphian','Christadelphian',8,9),(73,'','Christian','Christian',8,10),(74,'','Christian Other','Christian Other',8,11),(75,'','Christian Orthodox','Christian Orthodox',8,12),(76,'','Christian Scientist','Christian Scientist',8,13),(77,'','Church of Christ','Church of Christ',8,14),(78,'','Church of England','Church of England',8,15),(79,'','Church of God','Church of God',8,16),(80,'','Church of Ireland','Church of Ireland',8,17),(81,'','Church of Scotland','Church of Scotland',8,18),(82,'','Congregationalist','Congregationalist',8,19),(83,'','Episcopalian','Episcopalian',8,20),(84,'','Evangelical C of E','Evangelical C of E',8,21),(85,'','Free Church','Free Church',8,22),(86,'','Greek Orthodox','Greek Orthodox',8,23),(87,'','Hindu','Hindu',8,24),(88,'','Humanist','Humanist',8,25),(89,'','Islam','Islam',8,26),(90,'','Jain','Jain',8,27),(91,'','Jehovahs Witness','Jehovahs Witness',8,28),(92,'','Jewish','Jewish',8,29),(93,'','Lutheran','Lutheran',8,30),(94,'','Methodist','Methodist',8,31),(95,'','Moravian','Moravian',8,32),(96,'','Mormon','Mormon',8,33),(97,'','Muslim','Muslim',8,34),(98,'','New Life Church','New Life Church',8,35),(99,'','No Religion','No Religion',8,36),(100,'','None','None',8,37),(101,'','Not on List','Not on List',8,38),(102,'','Not Specified','Not Specified',8,39),(103,'','Other','Other',8,40),(104,'','Pagan','Pagan',8,41),(105,'','Pentecostal','Pentecostal',8,42),(106,'','Presbytarian','Presbytarian',8,43),(107,'','Presbyterian','Presbyterian',8,44),(108,'','Quaker','Quaker',8,45),(109,'','Rastafarian','Rastafarian',8,46),(110,'','Roman Catholic','Roman Catholic',8,47),(111,'','Russian Orthodox','Russian Orthodox',8,48),(112,'','Salvation Army','Salvation Army',8,49),(113,'','Scientologist','Scientologist',8,50),(114,'','Seventh Day Adventist','Seventh Day Adventist',8,51),(115,'','Sikh','Sikh',8,52),(116,'','Society Of Friends','Society Of Friends',8,53),(117,'','Spiritualist','Spiritualist',8,54),(118,'','Unitarian','Unitarian',8,55),(119,'','United Reform Church','United Reform Church',8,56),(120,'','Unknown','Unknown',8,57),(121,'','Witheld','Witheld',8,58),(122,'','M','Male',9,0),(123,'','F','Female',9,1),(124,'','I','Indeterminate',9,2),(125,'','NSP','Not Specified',9,3),(126,'','MDT Evidence','MDT Evidence',10,0),(127,'','Referral Letter','Referral Letter',10,1),(128,'','Test Results','Test Results',10,2),(129,'','Consultant Letter','Consultant Letter',10,3),(130,'','Consultant Annotations','Consultant Annotations',10,4),(131,'','Legal','Legal Reports',10,5),(132,'','Yes','Yes',11,0),(133,'','yes','yes',12,0),(134,'','no','no',12,1),(135,'','Yes','Yes',13,0),(136,'','No','No',13,1),(137,'','Left','Left',13,2),(138,'','Right','Right',13,3),(139,'','01','Yes',14,0),(140,'','02','No',14,1),(141,'','03','Other',14,2),(142,'','Yes','Yes',15,0),(143,'','No','No',15,1),(144,'','Right','Right',15,2),(145,'','Left','Left',15,3),(146,'','Yes','Yes',16,0),(147,'','No','No',16,1),(148,'','Suspicious','Suspicious',16,2),(149,'','Yes','Yes',17,0),(150,'','No','No',17,1),(151,'','Unknown','Unknown',17,2),(152,'','HPB','Hepatobilliary',18,0),(153,'','BRS','Breast',18,1),(154,'','GYN','Gynaecological',18,2),(155,'','HAE','Haematological',18,3),(156,'','HNK','Head and Neck',18,4),(157,'','LGI','Lower Gastro-Intestinal',18,5),(158,'','LUN','Lung',18,6),(159,'','OTH','Other tumour group',18,7),(160,'','SAR','Sarcoma',18,8),(161,'','SKN','Skin',18,9),(162,'','TST','Testicular',18,10),(163,'','UGI','Upper Gastro-Intestinal',18,11),(164,'','URO','Urological',18,12),(165,'','REC','Recovery',18,13),(166,'','Husband','Husband',19,0),(167,'','Wife','Wife',19,1),(168,'','Partner','Partner',19,2),(169,'','Mother','Mother',19,3),(170,'','Father','Father',19,4),(171,'','Sister ','Sister',19,5),(172,'','Brother ','Brother',19,6),(173,'','Son','Son',19,7),(174,'','Daughter','Daughter',19,8),(175,'','BRN','Brain / Central Nervous System',20,0),(176,'','BRS','Breast',20,1),(177,'','CAR','Cardiothoracic',20,2),(178,'','GEN','General',20,3),(179,'','GYN','Gynaecological',20,4),(180,'','HAE','Haematological',20,5),(181,'','HNK','Head and Neck',20,6),(182,'','HPB','Hepatobilliary',20,7),(183,'','LGI','Lower Gastro-Intestinal',20,8),(184,'','LUN','Lung',20,9),(185,'','OBS','Obesity',20,10),(186,'','OTH','Other tumour group',20,11),(187,'','SAR','Sarcoma',20,12),(188,'','SKN','Skin',20,13),(189,'','TST','Testicular',20,14),(190,'','UGI','Upper Gastro-Intestinal',20,15),(191,'','URO','Urological',20,16),(192,'','REC','Recovery',20,17),(193,'','CR','CR- Computed Radiography',21,0),(194,'','CT','CT - Computed Tomography',21,1),(195,'','MR','MRI - Magnetic Resonance Imaging',21,2),(196,'','US','US - Ultrasound',21,3),(197,'','NM','NM - Nuclear Medicine',21,4),(198,'','PT','PET - Positron Emission Tomography',21,5),(199,'','XA','AX - XRay Angiogram',21,6),(200,'','DX','DX - X-Ray',21,7),(201,'','MG','MG - Mammography X-Ray',21,8),(202,'','ECG','ECG -  Electrocardiogram',21,9),(203,'Global','0','Low',22,0),(204,'Global','1','Medium',22,1),(205,'Global','2','High',22,2),(206,'','Mr','Mr',23,0),(207,'','Mrs','Mrs',23,1),(208,'','Ms','Ms',23,2),(209,'','Miss','Miss',23,3),(210,'','Dr','Dr',23,4),(211,'','Prof','Professor',23,5),(212,'','Lord','Lord',23,6),(213,'','Lady','Lady',23,7),(214,'','Sir','Sir',23,8),(215,'','Dame','Dame',23,9),(216,'','Esq','Esq',24,0),(217,'','OBE','OBE',24,1),(218,'','MBE','MBE',24,2),(219,'','KG','KG',24,3),(220,'','Surgeon','Surgeon',25,0),(221,'','MedOncologist','Medical Oncologist',25,1),(222,'','ClinOnc','Clinical Oncologist',25,2),(223,'','CNS','CNS',25,3);
/*!40000 ALTER TABLE `pair` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `password_requests`
-- used to reset password via email, here the the url can be used only once and also token is validated by time
DROP TABLE IF EXISTS `password_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `password_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created_date` datetime(6) DEFAULT NULL,
  `is_password_updated` bit(1) DEFAULT NULL,
  `is_url_used` bit(1) DEFAULT NULL,
  `token` varchar(255) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UKhpa3qwp2ayui1odphjn0x5lml` (`token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `password_requests`
--

LOCK TABLES `password_requests` WRITE;
/*!40000 ALTER TABLE `password_requests` DISABLE KEYS */;
/*!40000 ALTER TABLE `password_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pathway`
-- defines the plan of treatment or actions to be followed, contains forms and summaries and
-- each subject can follow the pathway and will used used in the pathway metrics

DROP TABLE IF EXISTS `pathway`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pathway` (
  `pathway_id` int NOT NULL AUTO_INCREMENT,
  `creation_date` datetime(6) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `guid` varchar(255) NOT NULL,
  `interSiteName` varchar(255) NOT NULL,
  `isInterSitePathway` bit(1) NOT NULL,
  `modified_date` datetime(6) NOT NULL,
  `order_index` int DEFAULT NULL,
  `speciality` varchar(255) DEFAULT NULL,
  `title` varchar(100) NOT NULL,
  `created_by_user` int DEFAULT NULL,
  `modified_by_user` int DEFAULT NULL,
  PRIMARY KEY (`pathway_id`),
  UNIQUE KEY `UKbllxhyts2o3hf127sqno0r9fh` (`guid`),
  KEY `FKbja0qyle8m2pikqiyeywjthhj` (`created_by_user`),
  KEY `FKswk3jbrnaufvc3hx2hub44ho8` (`modified_by_user`),
  CONSTRAINT `FKbja0qyle8m2pikqiyeywjthhj` FOREIGN KEY (`created_by_user`) REFERENCES `users` (`user_id`),
  CONSTRAINT `FKswk3jbrnaufvc3hx2hub44ho8` FOREIGN KEY (`modified_by_user`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pathway`
--

LOCK TABLES `pathway` WRITE;
/*!40000 ALTER TABLE `pathway` DISABLE KEYS */;
/*!40000 ALTER TABLE `pathway` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pathway_form_map`
-- map of forms by name in the pathway
DROP TABLE IF EXISTS `pathway_form_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pathway_form_map` (
  `pathway_id` int NOT NULL,
  `Form_name` varchar(255) DEFAULT NULL,
  `formsSet_KEY` int NOT NULL,
  PRIMARY KEY (`pathway_id`,`formsSet_KEY`),
  KEY `FKg6ww4p0hfkf7p5djf1xy4hgls` (`formsSet_KEY`),
  CONSTRAINT `FKg6ww4p0hfkf7p5djf1xy4hgls` FOREIGN KEY (`formsSet_KEY`) REFERENCES `pathway_forms` (`pathway_form_id`),
  CONSTRAINT `FKqpwxf9wakd14agedqeb45kg9j` FOREIGN KEY (`pathway_id`) REFERENCES `pathway` (`pathway_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pathway_form_map`
--

LOCK TABLES `pathway_form_map` WRITE;
/*!40000 ALTER TABLE `pathway_form_map` DISABLE KEYS */;
/*!40000 ALTER TABLE `pathway_form_map` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pathway_form_summary_map`
--
-- map of forms and summaries by name in the pathway
DROP TABLE IF EXISTS `pathway_form_summary_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pathway_form_summary_map` (
  `pathway_FormSummary_id` int NOT NULL AUTO_INCREMENT,
  `afobject_id` int DEFAULT NULL,
  `form_or_summary_name` varchar(100) DEFAULT NULL,
  `group_name` varchar(255) NOT NULL,
  `location` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `summary_id` int DEFAULT NULL,
  `type` varchar(255) NOT NULL,
  PRIMARY KEY (`pathway_FormSummary_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pathway_form_summary_map`
--

LOCK TABLES `pathway_form_summary_map` WRITE;
/*!40000 ALTER TABLE `pathway_form_summary_map` DISABLE KEYS */;
/*!40000 ALTER TABLE `pathway_form_summary_map` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pathway_form_summary_map_order`
--
-- map of forms and summaries by name in the pathway holds the order
DROP TABLE IF EXISTS `pathway_form_summary_map_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pathway_form_summary_map_order` (
  `pathway_id` int NOT NULL,
  `pathway_form_summary_id` int NOT NULL,
  `child_index` int NOT NULL,
  PRIMARY KEY (`pathway_id`,`child_index`),
  KEY `FKfb7fkyno5wffvwtl5bkejne8k` (`pathway_form_summary_id`),
  CONSTRAINT `FK1j9nu255mn0mllialvrle7hpc` FOREIGN KEY (`pathway_id`) REFERENCES `pathway` (`pathway_id`),
  CONSTRAINT `FKfb7fkyno5wffvwtl5bkejne8k` FOREIGN KEY (`pathway_form_summary_id`) REFERENCES `pathway_form_summary_map` (`pathway_FormSummary_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pathway_form_summary_map_order`
--

LOCK TABLES `pathway_form_summary_map_order` WRITE;
/*!40000 ALTER TABLE `pathway_form_summary_map_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `pathway_form_summary_map_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pathway_forms`
--

DROP TABLE IF EXISTS `pathway_forms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pathway_forms` (
  `pathway_form_id` int NOT NULL AUTO_INCREMENT,
  `display_name` varchar(100) NOT NULL,
  `afobject_id` int NOT NULL,
  `group_name` varchar(100) DEFAULT NULL,
  `is_mandatory` bit(1) DEFAULT NULL,
  PRIMARY KEY (`pathway_form_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pathway_forms`
--  holds the details of the forms in the pathway
-- (used in metrics to see if the mandatory forms are filled and treatement plan is followed)
LOCK TABLES `pathway_forms` WRITE;
/*!40000 ALTER TABLE `pathway_forms` DISABLE KEYS */;
/*!40000 ALTER TABLE `pathway_forms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pathway_groups`
-- groups in a pathway , so forms belonging to the group appear under one button
DROP TABLE IF EXISTS `pathway_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pathway_groups` (
  `pathway_group_id` int NOT NULL AUTO_INCREMENT,
  `group_name` varchar(100) NOT NULL,
  `is_system` bit(1) NOT NULL,
  PRIMARY KEY (`pathway_group_id`),
  UNIQUE KEY `UK1foi4ig3widhkmewtuiw26fy2` (`group_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pathway_groups`
--

LOCK TABLES `pathway_groups` WRITE;
/*!40000 ALTER TABLE `pathway_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `pathway_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pathway_groups_map`
--  pathway has set of groups
DROP TABLE IF EXISTS `pathway_groups_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pathway_groups_map` (
  `pathway_id` int NOT NULL,
  `mandatory` bit(1) DEFAULT NULL,
  `groupMap_KEY` int NOT NULL,
  PRIMARY KEY (`pathway_id`,`groupMap_KEY`),
  KEY `FK3kffy78blyxcqvuwcv93afwj` (`groupMap_KEY`),
  CONSTRAINT `FK3kffy78blyxcqvuwcv93afwj` FOREIGN KEY (`groupMap_KEY`) REFERENCES `pathway_groups` (`pathway_group_id`),
  CONSTRAINT `FK5iij0hx4ns50pv68jp6ectjr4` FOREIGN KEY (`pathway_id`) REFERENCES `pathway` (`pathway_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pathway_groups_map`
--

LOCK TABLES `pathway_groups_map` WRITE;
/*!40000 ALTER TABLE `pathway_groups_map` DISABLE KEYS */;
/*!40000 ALTER TABLE `pathway_groups_map` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pathway_groups_map_order`
--
-- holds the order of the groups in the pathway
DROP TABLE IF EXISTS `pathway_groups_map_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pathway_groups_map_order` (
  `pathway_id` int NOT NULL,
  `pathway_group_id` int DEFAULT NULL,
  `groupMapOrder_KEY` int NOT NULL,
  PRIMARY KEY (`pathway_id`,`groupMapOrder_KEY`),
  CONSTRAINT `FKmhooyjkilyodj94ptdllc99cq` FOREIGN KEY (`pathway_id`) REFERENCES `pathway` (`pathway_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pathway_groups_map_order`
--

LOCK TABLES `pathway_groups_map_order` WRITE;
/*!40000 ALTER TABLE `pathway_groups_map_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `pathway_groups_map_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pathway_summaries`
--
-- details of the summaries in the pathway
DROP TABLE IF EXISTS `pathway_summaries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pathway_summaries` (
  `pathway_id` int NOT NULL,
  `summary_name` varchar(255) DEFAULT NULL,
  `summaries_KEY` int NOT NULL,
  PRIMARY KEY (`pathway_id`,`summaries_KEY`),
  KEY `FKjtf2dsldhe8kejvimtmm0w7yh` (`summaries_KEY`),
  CONSTRAINT `FK6qa5c7lrk6hv9fgtyaecxqdy2` FOREIGN KEY (`pathway_id`) REFERENCES `pathway` (`pathway_id`),
  CONSTRAINT `FKjtf2dsldhe8kejvimtmm0w7yh` FOREIGN KEY (`summaries_KEY`) REFERENCES `summary` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pathway_summaries`
--

LOCK TABLES `pathway_summaries` WRITE;
/*!40000 ALTER TABLE `pathway_summaries` DISABLE KEYS */;
/*!40000 ALTER TABLE `pathway_summaries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pathway_users`
-- users listed in a pathway by organisations
DROP TABLE IF EXISTS `pathway_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pathway_users` (
  `organisation_pathway_id` int NOT NULL,
  `user_id` int NOT NULL,
  `child_index` int NOT NULL,
  PRIMARY KEY (`organisation_pathway_id`,`child_index`),
  KEY `FK5bif2smajnom219b6ay8pu6fw` (`user_id`),
  CONSTRAINT `FK5bif2smajnom219b6ay8pu6fw` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `FKqrpa52ai4ug175jramyg4td61` FOREIGN KEY (`organisation_pathway_id`) REFERENCES `organisation_pathways` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pathway_users`
--

LOCK TABLES `pathway_users` WRITE;
/*!40000 ALTER TABLE `pathway_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `pathway_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_care_providers`
-- not used yet

DROP TABLE IF EXISTS `patient_care_providers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient_care_providers` (
  `careProvider_id` int NOT NULL,
  `identifier` varchar(255) DEFAULT NULL,
  `careProviderDetailsMap_KEY` int NOT NULL,
  PRIMARY KEY (`careProvider_id`,`careProviderDetailsMap_KEY`),
  KEY `FKt4wynixow4l5wblji68ara4b` (`careProviderDetailsMap_KEY`),
  CONSTRAINT `FKikrai7d7jqsyavingh5pv4uma` FOREIGN KEY (`careProvider_id`) REFERENCES `subject` (`subject_id`),
  CONSTRAINT `FKt4wynixow4l5wblji68ara4b` FOREIGN KEY (`careProviderDetailsMap_KEY`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_care_providers`
--

LOCK TABLES `patient_care_providers` WRITE;
/*!40000 ALTER TABLE `patient_care_providers` DISABLE KEYS */;
/*!40000 ALTER TABLE `patient_care_providers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `principal`
--  related to acl

DROP TABLE IF EXISTS `principal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `principal` (
  `principal_type` varchar(31) NOT NULL,
  `principal_id` int NOT NULL AUTO_INCREMENT,
  `principal_name` varchar(255) NOT NULL,
  `principal_unique` varchar(255) NOT NULL,
  PRIMARY KEY (`principal_id`),
  UNIQUE KEY `UKowsi2cor3xuujyw9pemo1xayt` (`principal_unique`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `principal`
--

LOCK TABLES `principal` WRITE;
/*!40000 ALTER TABLE `principal` DISABLE KEYS */;
/*!40000 ALTER TABLE `principal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `program`
-- the patient/subject is imported from PAS belongs to a clinic/program

DROP TABLE IF EXISTS `program`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `program` (
  `program_id` int NOT NULL AUTO_INCREMENT,
  `program_group_code` varchar(50) NOT NULL,
  `program_date` datetime(6) DEFAULT NULL,
  `consultant_code` varchar(50) DEFAULT NULL,
  `consultant_forename` varchar(50) DEFAULT NULL,
  `consultant_surname` varchar(50) DEFAULT NULL,
  `institution_code` varchar(50) DEFAULT NULL,
  `speciality` varchar(50) NOT NULL,
  PRIMARY KEY (`program_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program`
--

LOCK TABLES `program` WRITE;
/*!40000 ALTER TABLE `program` DISABLE KEYS */;
/*!40000 ALTER TABLE `program` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `program_subject`
-- each clinic/program can have a list of patients/sunjects

DROP TABLE IF EXISTS `program_subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `program_subject` (
  `program_id` int NOT NULL,
  `subject_id` int NOT NULL,
  `child_index` int NOT NULL,
  PRIMARY KEY (`program_id`,`child_index`),
  KEY `FKixwb6nirxkn0h0jjmk54iv6l2` (`subject_id`),
  CONSTRAINT `FK6u3q288n6sweoanwg12pyp2qm` FOREIGN KEY (`program_id`) REFERENCES `program` (`program_id`),
  CONSTRAINT `FKixwb6nirxkn0h0jjmk54iv6l2` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`subject_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program_subject`
--

LOCK TABLES `program_subject` WRITE;
/*!40000 ALTER TABLE `program_subject` DISABLE KEYS */;
/*!40000 ALTER TABLE `program_subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `provider_details`
-- holds the  details of all the user associated with the subject/patient
-- (even if the user doesn't exists in the system , when referred from other organisation)

DROP TABLE IF EXISTS `provider_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `provider_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_date` datetime(6) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `email_address` varchar(255) DEFAULT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `organisation_code` varchar(255) DEFAULT NULL,
  `organisation_name` varchar(255) DEFAULT NULL,
  `mobile_phone` varchar(255) DEFAULT NULL,
  `subject_identifier` varchar(255) DEFAULT NULL,
  `postcode` varchar(255) DEFAULT NULL,
  `role` varchar(255) DEFAULT NULL,
  `speciality` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `work_phone` varchar(255) DEFAULT NULL,
  `subject_id` int DEFAULT NULL,
  `child_index` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FKld09343qrpjkmk8u6yrmft0w3` (`subject_id`),
  CONSTRAINT `FKld09343qrpjkmk8u6yrmft0w3` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`subject_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `provider_details`
--

LOCK TABLES `provider_details` WRITE;
/*!40000 ALTER TABLE `provider_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `provider_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `referrals`
-- holds the referral details of a subject

DROP TABLE IF EXISTS `referrals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `referrals` (
  `referral_id` int NOT NULL AUTO_INCREMENT,
  `acknowledgement_date` datetime(6) DEFAULT NULL,
  `guid` varchar(255) NOT NULL,
  `image_transport` varchar(50) DEFAULT NULL,
  `manual_tracking` bit(1) DEFAULT NULL,
  `registered` bit(1) DEFAULT NULL,
  `referral_date` datetime(6) DEFAULT NULL,
  `referral_method` int DEFAULT NULL,
  `referral_mode` int DEFAULT NULL,
  `referral_notes` varchar(255) DEFAULT NULL,
  `referral_status` int NOT NULL,
  `referring_from_organisation` int NOT NULL,
  `referring_specialist_address` varchar(500) DEFAULT NULL,
  `referring_specialist_fax` varchar(20) DEFAULT NULL,
  `referring_specialist_org_code` varchar(255) DEFAULT NULL,
  `referring_specialist_jobtitle` varchar(255) DEFAULT NULL,
  `referring_specialist_name` varchar(255) DEFAULT NULL,
  `referring_specialist_postcode` varchar(20) DEFAULT NULL,
  `referring_specialist_telephone` varchar(20) DEFAULT NULL,
  `referring_specialist_username` varchar(255) DEFAULT NULL,
  `referring_to_organisation` int DEFAULT NULL,
  `response_date` datetime(6) DEFAULT NULL,
  `team` bit(1) DEFAULT NULL,
  `tracking` varchar(255) DEFAULT NULL,
  `episode_id` int NOT NULL,
  `pathway_id` int DEFAULT NULL,
  `referred_from_user_id` int DEFAULT NULL,
  `referred_to_user_id` int DEFAULT NULL,
  `referring_specialist_user_id` int DEFAULT NULL,
  `child_index` int DEFAULT NULL,
  PRIMARY KEY (`referral_id`),
  UNIQUE KEY `UKlu1hi1x9voedregiociej06lt` (`guid`),
  KEY `FKo22ffytfdnafax444ekd7otna` (`episode_id`),
  KEY `FK2b8fhmo7baosxga5v7gxq9lg1` (`pathway_id`),
  KEY `FKhgirlxca6pqpj9og3pw736lej` (`referred_from_user_id`),
  KEY `FK476jbbhw7bsoh32ltk87dw3vs` (`referred_to_user_id`),
  KEY `FK6su0dfrwa9yfmub27a6jwv3rh` (`referring_specialist_user_id`),
  CONSTRAINT `FK2b8fhmo7baosxga5v7gxq9lg1` FOREIGN KEY (`pathway_id`) REFERENCES `pathway` (`pathway_id`),
  CONSTRAINT `FK476jbbhw7bsoh32ltk87dw3vs` FOREIGN KEY (`referred_to_user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `FK6su0dfrwa9yfmub27a6jwv3rh` FOREIGN KEY (`referring_specialist_user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `FKhgirlxca6pqpj9og3pw736lej` FOREIGN KEY (`referred_from_user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `FKo22ffytfdnafax444ekd7otna` FOREIGN KEY (`episode_id`) REFERENCES `episode` (`episode_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `referrals`
--

LOCK TABLES `referrals` WRITE;
/*!40000 ALTER TABLE `referrals` DISABLE KEYS */;
/*!40000 ALTER TABLE `referrals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_menuitem`
-- each role has a set of menu items
-- which the user will see onweb login based on the roles assigned to the user

DROP TABLE IF EXISTS `role_menuitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role_menuitem` (
  `role_id` int NOT NULL,
  `menuitem_id` int NOT NULL,
  PRIMARY KEY (`role_id`,`menuitem_id`),
  KEY `FK90iln72hrokonbvyer68v4xka` (`menuitem_id`),
  CONSTRAINT `FK90iln72hrokonbvyer68v4xka` FOREIGN KEY (`menuitem_id`) REFERENCES `menu_item` (`id`),
  CONSTRAINT `FKiu7qvefk9ul0u5eqm7adiqsvr` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_menuitem`
--

LOCK TABLES `role_menuitem` WRITE;
/*!40000 ALTER TABLE `role_menuitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `role_menuitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_usernames`
-- users and roles map

DROP TABLE IF EXISTS `role_usernames`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role_usernames` (
  `role_id` int NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  KEY `FKtktsvx4162u2vfi7c1j1twmu8` (`role_id`),
  CONSTRAINT `FKtktsvx4162u2vfi7c1j1twmu8` FOREIGN KEY (`role_id`) REFERENCES `principal` (`principal_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_usernames`
--

LOCK TABLES `role_usernames` WRITE;
/*!40000 ALTER TABLE `role_usernames` DISABLE KEYS */;
/*!40000 ALTER TABLE `role_usernames` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
-- stores the roles that exists in the system

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `description` varchar(2000) DEFAULT NULL,
  `is_desktop` bit(1) DEFAULT NULL,
  `enabled` bit(1) NOT NULL,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`role_id`),
  UNIQUE KEY `UKhe2epnojwl1f3jxagv2mdsv3v` (`value`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'System',_binary '',_binary '','ROLE_ADMIN'),(2,'eMDT',_binary '',_binary '','ROLE_EMDT'),(3,'Calendar',_binary '',_binary '','ROLE_CALENDAR'),(4,'Meetings',_binary '',_binary '','ROLE_MEETINGS'),(5,'Activity',_binary '',_binary '','ROLE_SUMMARY'),(6,'User can access all patient records irrespective of care role',_binary '\0',_binary '','ROLE_ACCESS_ALL_PATIENTS'),(7,'Refer Patient',_binary '',_binary '','ROLE_REFERRAL'),(8,'Referrals Management',_binary '',_binary '','ROLE_MANAGEMENT'),(9,'User can receive patient referrals',_binary '\0',_binary '','ROLE_RECEIVE_REFERRAL'),(10,'User can cancel draft patient referrals',_binary '\0',_binary '','ROLE_REFERRAL_SUPERVISOR'),(11,'Meeting administrator privileges',_binary '\0',_binary '','ROLE_MEETING_ADMIN'),(12,'Managed MDM',_binary '',_binary '','ROLE_NMDT_COORD'),(13,'User can submit patient to MDT Meeting',_binary '\0',_binary '','ROLE_NMDM_SUBMITTER'),(14,'Patient Portal',_binary '',_binary '','ROLE_PATIENT');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service_transaction_info`
-- used to validate trasactions for the older api's

DROP TABLE IF EXISTS `service_transaction_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service_transaction_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created_date` datetime(6) DEFAULT NULL,
  `session_key` varchar(255) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UKmg3n6wrflukwvkt06nghqa9g6` (`session_key`),
  KEY `FKm7egpd7n6fi6461voo8bprv6t` (`user_id`),
  CONSTRAINT `FKm7egpd7n6fi6461voo8bprv6t` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_transaction_info`
--

LOCK TABLES `service_transaction_info` WRITE;
/*!40000 ALTER TABLE `service_transaction_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `service_transaction_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `settings`
-- Purpose: Stores configuration properties that were originally in a properties file.
-- Each row represents a key-value pair used for application settings.

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` varchar(256) DEFAULT NULL,
  `Property_key` varchar(256) NOT NULL,
  `Property_value` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UKa7j4a1okj1sxip7l9hm3mt0h3` (`Property_key`)
) ENGINE=InnoDB AUTO_INCREMENT=192 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `settings`
--

LOCK TABLES `settings` WRITE;
/*!40000 ALTER TABLE `settings` DISABLE KEYS */;
INSERT INTO `settings` VALUES (1,'Time when PAS update process will run. Format: CRON expression','auto.pas.update.schedule','0 0 0 * * ?'),(2,'Time when calendar reminders process will run. Format: CRON expression','calendarreminder.time','0 0 * * * ?'),(3,'Interval in minutes for calendar reminders','calendarreminderdate.time','60'),(4,'Closing quote character for escaping database fields. ` for MySQL or ] for SQL Server','closequote','`'),(5,'Physical directory name on server in which to store documents uploaded and attached to comments\n        ','comments.notes.upload.dir','{server.data.root}/notes_attachments'),(6,'Mnemonic speciality code to be used by default for new patients','defaultCareSpell','BRS'),(7,'Time period in days after which to warn of delayed referral acknowledgements','emdt.acknowledgement.notification.elapsed.days','2'),(8,'Time when referrals acknowledgement reminders will be sent. Format: CRON expression','emdt.acknowledgement.notification.interval','0 0 10 * * ?'),(9,'Flag for whether we should display a link for prospective users to apply for login accounts.\n            Values: true or false\n        ','emdt.allow.account.applications','false'),(10,'Enable queries for patient demographics in PAS. Values: true or false','emdt.allow.patient.lookup','true'),(11,'Relative pathname of JSP used for rendering a consultation note for PDF','emdt.archive.patientDetails.JspFormDataConvertedTopdf','emdt/archivePatientDetailsView.jsp'),(12,'Flag for whether patient details should be archived to TEXT after every change. Caution: impacts\n            performance. Values: true or false\n        ','emdt.archive.text.enabled','false'),(13,'Physical directory on server for archiving TXT representations of patient forms.','emdt.archive.text.location','{server.data.root}/archive/text/'),(14,'Flag for whether patient details should be archived to PDF after every change. Caution: impacts\n            performance. Values: true or false\n        ','emdt.archive.pdf.enabled','false'),(15,'Physical directory on server for archiving PDF representations of patient forms.','emdt.archive.pdf.location','{server.data.root}/archive/pdf/'),(16,'Flag for whether patient details should be archived to XML after every change. Caution: impacts\n            performance. Values: true or false\n        ','emdt.archive.xml.enabled','false'),(17,'Physical directory on server for archiving XML representations of patient forms.','emdt.archive.xml.location','{server.data.root}/archive/xml/'),(18,'Form Editor domain and group name used for creating referrals forms','emdt.referrals.uniqueStringPath','/EMDT/Referrals/'),(19,'Deprecated.','emdt.default.referral.method','0'),(20,'Mnemonic speciality code to be used by default for new patient referrals','emdt.default.referral.speciality','{defaultCareSpell}'),(21,'Form Editor domain, group and form name used for creating referral response forms','emdt.default.response.form','/EMDT/Referrals/Response'),(22,'Flag to determine if reporting export database should be updated after each change. Caution: may\n            impact performance. Values: true or false\n        ','emdt.export.autoexport','false'),(23,'JDBC driver classname for reporting database','emdt.export.dbClass','com.mysql.cj.jdbc.Driver'),(24,'JDBC password for reporting database','emdt.export.dbPassword','76b25d190b1060eb41c41f9dadd3fcc4'),(25,'JDBC connection URL for reporting database','emdt.export.dbUrl','jdbc:mysql://localhost:3306/emdtreporting?autoReconnect=true&useSSL=false&allowPublicKeyRetrieval=true'),(26,'JDBC username for reporting database','emdt.export.dbUserID','emdtexport'),(27,'Flag for exporting to NBOCAP audit. Deprecated.','emdt.export.nbocap.enable','false'),(28,'Flag for exporting to CWT audit. Values: true or false','emdt.feed.cancerreferrals.enable','false'),(29,'Physical directory path on server in which to upload files uploaded and attached to forms.\n        ','emdt.form.editor.upload.dir','{server.data.root}/FileUploads/'),(30,'Time when IEP image transfer status update process will run. Format: CRON expression','emdt.iep.image.transfer.status','0 0 0 * * ?'),(31,'Flag to automatically select the next meeting when adding a patient to a meeting. Values: true or\n            false\n        ','emdt.meeting.autoselect.current','false'),(32,'Flag to show the image requests within the meeting discussion. Values: true or false','emdt.meeting.imaging.enabled','true'),(33,'Relative pathname of JSP used for rendering a patient meeting discussion for PDF','emdt.meeting.invitation.attachJspToBeConvertedToPdf','meetings/printPatientsInCurrentMeeting.jsp'),(34,'Originating email address for outbound mail from meeting invitations.','emdt.meeting.invitation.from','{webapp.email.from}'),(35,'Server name to include in .ICS files','emdt.meeting.invitation.ical.uid.host','{server.name}'),(36,'Flag determining if patient details (PID) are to be included in outbound email messages. Values:\n            true or false\n        ','emdt.meeting.invitation.includePatientDetails','true'),(37,'SMTP server address for outbound email from meetings','emdt.meeting.invitation.smtp.host','{webapp.smtp.host}'),(38,'Optional: system folder containing True Type font files, used for rendering PDFs. Format: physical\n            server path\n        ','emdt.meeting.pdfgenerate.fontUploadDirectory','/Library/Fonts'),(39,'Flag to mask PID when sending emails. If true, PID is replaced with asterisks. Values: true o\n            false\n        ','emdt.messaging.maskPatientDetails','false'),(40,'Time when delayed image transfers will be checked. Format: CRON expression','emdt.notification.delay.image.transfer','0 0 * * * ?'),(41,'Time when escalated reminders will be sent. Format: CRON expression','emdt.notification.escalation.schedule','0 0 2 * * ?'),(42,'Originating email address for outbound mail from meeting invitations.','emdt.notification.invitation.from','{webapp.email.from}'),(43,'SMTP server address for outbound email from notifications','emdt.notification.smtp.host','{webapp.smtp.host}'),(44,'Flag to allow user to manually enter patient demographics details. Values: true or false\n        ','emdt.patient.can.create','true'),(45,'Flag to allow user to edit patient demographics details. Values: true or false','emdt.patient.details.editable','true'),(46,'Physical directory path on server where patient files are stored','emdt.patientFilesUrl','{server.data.root}/patientfiles'),(47,'If set to true, patient demographics are automatically refreshed via SQL PAS feed on patient\n            selection. Values: true or false\n        ','emdt.patientInfo.autoPASUpdate','false'),(48,'Flag to allow user to edit patient demographics details. Values: true or false','emdt.patientInfo.readonly','false'),(49,'Flag to display extra demographics panel in Patient Details screen. Values: true or false\n        ','emdt.patientInfo.showExtraDemographics','true'),(50,'Flag to display next of kin panel in Patient Details screen. Values: true or false','emdt.patientInfo.showNextOfKin','true'),(51,'Flag to display allergies panel in Patient Details screen. Values: true or false','emdt.patientInfo.showAllergies','true'),(52,'Time period in days after which to warn of delayed referrals','emdt.referral.notification.elapsed.days','2'),(53,'Originating email address for outbound mail from referral invitations.','emdt.referral.notification.email.from','{webapp.email.from}'),(54,'Time when referrals notification reminders will be sent. Format: CRON expression','emdt.referral.notification.interval','0 0 10 * * ?'),(55,'JDBC driver classname for SQL reporting database','emdt.report.dbClass','com.mysql.cj.jdbc.Driver'),(56,'JDBC password for SQL reporting database','emdt.report.dbPassword','4e0caffe847a5c308ff6912ba3088d95'),(57,'JDBC connection URL for SQL reporting database','emdt.report.dbUrl','jdbc:mysql://localhost:3306/emdtreporting?autoReconnect=true&useSSL=false&allowPublicKeyRetrieval=true'),(58,'JDBC username for SQL reporting database','emdt.report.dbUserID','emdtreports'),(59,'Flag for enabling export to reporting database. Caution: may impact performance. Values: true or\n            false.\n        ','emdt.reporting.export.enabled','false'),(60,'Time when reporting export database will be refreshed. Format: CRON expression','emdt.reporting.export.process.schedule','0 0 1 * * ?'),(61,'Internal use only','emdt.server.emdtService.url','{server.url}webservices/emdtService'),(62,'Internal use only','emdt.server.mergepatient.service.url','{server.url}webservices/mergePatient'),(63,NULL,'emdt.server.rest.emdtService.url','{server.url}webservices/rest/emdtService/'),(64,'Physical path on server where SQL queries file will be stored','emdt.sqlquery.saved.location','{server.data.root}/SavedSqlQueries.txt'),(65,'Flag to require users to use a strong password. Values: true or false','enforce.strong.password','true'),(66,'Number of scheduled meetings per meeting schedule to display when patient is added to a meeting.\n            Values: integer greater than 0\n        ','futureMeetingsToCreate','4'),(67,'Originating email address for outbound mail for imaging notifications.','imaging.sysadmin.notification.email.address','your.email.address@mail.com'),(68,'Flag to enable LDAP or Active Directory user authentication. Values: true or false','ldap.authentication.service.isActivated','false'),(69,'LDAP or Active Directory domain name','ldap.domain.names','your_domain'),(70,NULL,'management.endpoint.health.show-details','always'),(71,NULL,'management.endpoints.web.exposure.include','*'),(72,'Title for meetings that are created via automatic referral patient bookings','mdtBookingForm.defaultMeetingTitle','Automatically booked'),(73,'','mdtBookingForm.formFieldKey.meetingDate','MeetingDate'),(74,'','mdtBookingForm.formFieldKey.meetingId','MeetingId'),(75,'','mdtBookingForm.formFieldKey.meetingItemType','PatientReasonforDiscussion'),(76,'','mdtBookingForm.formFieldKey.meetingSpeciality','NewMeetingSpeciality'),(77,'','mdtBookingForm.formFieldKey.meetingTime','MeetingTime'),(78,'','mdtBookingForm.formFieldKey.meetingTitle','MeetingTitle'),(79,'Form Editor path name for form used for automatic meeting bookings for referral patients\n        ','mdtBookingForm.formName','/EMDT/Forms/MDTRegistration'),(80,'Opening quote character for escaping database fields. ` for MySQL or [ for SQL Server','openquote','`'),(81,'Flag for allowing passwords to expire after a number of days. Values: true or false','password.can.expire','false'),(82,'Number of days after which passwords expire. Used only if setting password.can.expire is true.\n            Values: integer\n        ','password.expiry.age','45'),(83,'Passwords should include non-alphabetic characters. Values: true or false','password.include.non-alpha','false'),(84,'Passwords should include numeric characters. Values: true or false','password.include.numeric','false'),(85,'Passwords should include upper-case characters. Values: true or false','password.include.uppercase','false'),(86,'Passwords minimum length. Values: integer, defaults to 8','password.minimum.length','8'),(87,'','password.warning.age','5'),(88,'Maximum number of patients to show in search results','patients.maxlimit','1000'),(89,'Relative pathname of JSP used for rendering a patient form for PDF','referrals.archive.JspFormDataConvertedTopdf','referrals/archiveFormView.jsp'),(90,'Relative pathname of JSP used for rendering patient demographics for PDF','referrals.archive.patientDetails.JspFormDataConvertedTopdf','referrals/archivePatientDetailsView.jsp'),(91,'Deprecated','referrals.imageview.folder.name','patient-images'),(92,'Deprecated','referrals.print.folder','{server.data.root}/PrintPDF/'),(93,'Deprecated','referrals.print.temp.folder','{server.data.root}/TempPrintPDF/'),(94,'SMTP server address for outgoing mail from referrals','referrals.smtp.host','{webapp.smtp.host}'),(95,NULL,'registration_form_url','http://emdt.net/eMDTReg/regForm.jsp'),(96,'Physical directory on server used as parent folder for application data storage','server.data.root','/var/emdtdata/{webapp.name}'),(97,'Network hostname of eMDT server','server.name','dev.ardeo.net'),(98,NULL,'server.port','8080'),(99,'Web URL of this eMDT application, used in outbound emails. Format: URL','server.url','https://{server.name}/{webapp.name}/'),(100,'Maximum size of file that may be uploaded to server','spring.http.multipart.maxFileSize','100000000'),(101,NULL,'spring.jackson.serialization.fail-on-empty-beans','false'),(102,'Number of failed login attempts allowed before account is temporarily locked. Format: integer\n        ','user.account.lockout.threshold','3'),(103,'Originating email address for outbound SMTP mail.','webapp.email.from','noreply@ardeo.com'),(104,NULL,'webapp.filters.SessionCheckFilter.ignore','/{webapp.name}/login /{webapp.name}/webapp-js.jsp favicon.ico'),(105,NULL,'webapp.filters.SessionCheckFilter.loginUrl','/{webapp.name}/login'),(106,NULL,'webapp.filters.WebAppFilter.timer.enabled','true'),(107,'Web app context name','webapp.name','emdtcloud'),(108,'Originating email address for outbound mail from meeting invitations.','webapp.sendreferral.success.email.from','{webapp.email.from}'),(109,'Boolean flag for enabling authentication for outbound SMTP email. Values: true or false\n        ','webapp.smtp.authentication','true'),(110,'Domain name or IP address of SMTP server for outbound email','webapp.smtp.host','secure.emailsrvr.com'),(111,'Password for SMTP server outbound email, required if authentication is enabled','webapp.smtp.password','Pipegripestripe30102020!'),(112,'TCP port of SMTP server for outbound email','webapp.smtp.port','465'),(113,'Protocol name for SMTP outbound email','webapp.smtp.protocol','smtps'),(114,'Boolean flag to enable STARTTLS for SMTP outbound email','webapp.smtp.starttls.enable','true'),(115,'Username for authenticating outbound email connection to SMTP server. Defaults to originating email\n            address. Required if authentication is enabled\n        ','webapp.smtp.username','{webapp.email.from}'),(116,NULL,'webshare.base.url','/webshare/'),(117,'Physical path to directory on server where files uploaded via the System File Sharing feature will\n            be stored\n        ','webshare.folder.path','{server.data.root}/webshare/'),(118,'Internal: Mirth interface REST address for appointments query','emdt.appointments.rest.address','http://127.0.0.1:8089/queryAppointments/?patientId'),(119,NULL,'emdt.pas.dao.impl','com.ardeo.emdt.dao.hibernate.HibernatePASDataDAO'),(120,'Flag to administratively enable or disable patient lookups based on patient hospital number/ID.  Values: true or false.','emdt.pas.enabled','false'),(121,'Internal: Mirth interface REST address for PAS query','emdt.pas.rest.address','http://127.0.0.1:8087/queryPas/?patientId='),(122,'Deprecated','pas.initialisation.query',''),(123,'Deprecated','emdt.imaging.impl','com.ardeo.emdt.imaging.bbrad.BBRadImagingInterface'),(124,'Flag for enabling bbRad image requests. Values: true or false','bbrad.enabled','false'),(125,'SOAP namespace of IEP web service','iep.namespaceUrl','https://nww.iepservice.nhs.uk/API/2010/10/10/'),(126,'Password for accessing IEP service','iep.password','your.iep.password'),(127,'Do not edit: Internal use only','iep.status.accepted','IMAGE_STATUS_SENT_TRANSFERINPROGRESS'),(128,'Do not edit: Internal use only','iep.status.acknowledge','IMAGE_STATUS_SENT_TRANSFERINPROGRESS'),(129,'Do not edit: Internal use only','iep.status.authorised','IMAGE_STATUS_SENT_TRANSFERINPROGRESS'),(130,'Do not edit: Internal use only','iep.status.availableoniep','IMAGE_STATUS_SENT_TRANSFERINPROGRESS'),(131,'Do not edit: Internal use only','iep.status.awaitingreport','IMAGE_STATUS_SENT_TRANSFERINPROGRESS'),(132,'Do not edit: Internal use only','iep.status.cancelled','IMAGE_STATUS_TRANSFERCANCELED'),(133,'Do not edit: Internal use only','iep.status.decline','IMAGE_STATUS_TRANSFERCANCELED'),(134,'Do not edit: Internal use only','iep.status.delivered','IMAGE_STATUS_ARRIVED_TRANSFERCOMPLETED'),(135,'Do not edit: Internal use only','iep.status.downloading','IMAGE_STATUS_SENT_TRANSFERINPROGRESS'),(136,'Do not edit: Internal use only','iep.status.downloadrequested','IMAGE_STATUS_SENT_TRANSFERINPROGRESS'),(137,'Do not edit: Internal use only','iep.status.failed','IMAGE_STATUS_TRANSFERFAILED'),(138,'Do not edit: Internal use only','iep.status.forwarded','IMAGE_STATUS_SENT_TRANSFERINPROGRESS'),(139,'Do not edit: Internal use only','iep.status.locked','IMAGE_STATUS_TRANSFERFAILED'),(140,'Do not edit: Internal use only','iep.status.new','IMAGE_STATUS_REQUESTED'),(141,'Do not edit: Internal use only','iep.status.packedcollected','IMAGE_STATUS_ARRIVED_TRANSFERCOMPLETED'),(142,'Do not edit: Internal use only','iep.status.purged','IMAGE_STATUS_TRANSFERFAILED'),(143,'Do not edit: Internal use only','iep.status.reportreceived','IMAGE_STATUS_SENT_TRANSFERINPROGRESS'),(144,'Do not edit: Internal use only','iep.status.started','IMAGE_STATUS_SENT_TRANSFERINPROGRESS'),(145,'Do not edit: Internal use only','iep.status.uploading','IMAGE_STATUS_SENT_TRANSFERINPROGRESS'),(146,'Username for accessing IEP service','iep.username','your.iep.username'),(147,'Vendor code for accessing IEP service','iep.vendorcode','your.iep.vendor.code'),(148,'Do not edit: Internal use only','iep.wsdlUrl','https://uat.pacsportal.co.uk/IEP/api.asmx?wsdl'),(149,'Does PACS server support CGET DICOM command? Values: true or false','pacs.cget.is.supported','true'),(150,'PACS timeout in milliseconds','pacs.dcmche.get.image.timeout.ms','1000000'),(151,'DICOM AET of PACS','pacs.emdt.aet.name','DCMQR'),(152,'DICOM hostname or IP address of PACS server. Values: hostname or IP address of PACS','pacs.emdt.server.bind.address','localhost'),(153,'PACS server TCP port for DICOM service','pacs.emdt.server.port','5104'),(154,'PACS AET of this local DICOM node used for forming associations with PACS','pacs.local.aet.name','DCM4CHEE'),(155,'PACS server name of this local DICOM node used for forming associations with PACS. Normally the\n            hostname or IP address of this server\n        ','pacs.local.server.name','your.pacs.server'),(156,'PACS TCP port of this local DICOM node used for forming associations with PACS','pacs.local.server.port','11112'),(157,'Hostname of bbRad service','bbrad.server.address','81.179.236.104'),(158,'TCP port of bbRad service','bbrad.server.port','1103'),(159,'Flag to enable bbRad image tracking. Values: true or false','bbrad.status.tracking.enabled','false'),(160,'TCP port of listening server socket for inbound bbRad communications','bbrad.status.tracking.listener.port','1103'),(161,'Internal use only: do not edit','pathologyFeed.dao.impl','com.ardeo.emdt.feeds.pathologyFeed.dao.HibernateSpirePathologyDAO'),(162,'Flag for enabling pathology DAO interface','pathologyFeed.enabled','false'),(163,'Form Editor pathname of for used for storing imported pathology results','pathology.results.feed.form.path','/EMDT/Results/PathologyResults'),(164,'Flag for enabling two factor authentication (2FA). Values: true or false','emdt.enable.2FA','True'),(165,'Add DEBUG SMTP conversations to log file','webapp.mail.debug','true'),(166,'Hostname or IP address of server hosting visual meetings service','jitsi.meetingRoom.domain','av.dev.ardeo.net'),(167,'Flag for enforcing two factor authentication (2FA) is used. Values: true or false','emdt.enforce.2FA','False'),(168,'customer logo','customer.logo.filename','ardeo-emdt.jpg'),(169,'customer company name','customer.companyname','Ardeo Ltd'),(170,'customer address','customer.address','Kingston upon Thames'),(171,NULL,'emdt.basingstoke.uniqueStringPath','/EMDT/Referrals/'),(172,'DicomWeb server URL','pacs.dicomweb.url','https://dev.ardeo.net/orthanc/'),(173,'DicomWeb username','pacs.dicomweb.user','pacsadmin'),(174,'DicomWeb password','pacs.dicomweb.password','bean1908chutney.'),(175,'path to save user profile picture','user.profile.picture.folder.path','{server.data.root}/userprofile'),(176,'wsdl publish location','webservices.wsdlurl','http://localhost:8081/emdt/webservices/'),(177,'default pathway title for mobile clinicians','default.pathway.title','Default'),(178,'Physical directory name on server in which to store documents uploaded and attached to user\n            comments\n        ','user.chat.upload.dir','{server.data.root}/notes_attachments'),(179,'emdt audio/video call will expire in hours','emdt.video.call.expiry.hours','24'),(180,'Internal: Spring bean name for PAS service','emdt.pas.service.name','restPasDataService'),(181,'enable ssl when sending emails','webapp.smtp.ssl.enable','true'),(182,'imap port','webapp.imap.port','993'),(183,'emdt notification mail address','emdt.mail.username','mailhub@healthvive.com'),(184,'emdt notification mail password','emdt.mail.password','PLORASteam.0111!'),(185,'limit the users shown in notifications list to hub and referral.','webapp.filter.user.notification','false'),(186,'Enable to find patient from database using nhsnumber. Values: true or false','emdt.allow.patient.nhsnumber.lookup','true'),(187,'eMDT UI vocabulary','emdt.industry','default'),(188,'Registration - automatic activations','registrations.automatic.activations','true'),(189,'Flag to display the sex panel in Patient Details screen. Values: true or false','emdt.patientInfo.showSex','true'),(190,'hexString used to produce checksum','webapp.checksum.algorithm.hexString','%064x'),(191,'algorithm used to produce checksum','webapp.checksum.algorithm','SHA-256');
/*!40000 ALTER TABLE `settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `speciality`
--

DROP TABLE IF EXISTS `speciality`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `speciality` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` int NOT NULL,
  `description` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `speciality`
-- not used

LOCK TABLES `speciality` WRITE;
/*!40000 ALTER TABLE `speciality` DISABLE KEYS */;
/*!40000 ALTER TABLE `speciality` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subject`
-- details of the subject (patient or project, we will be calculating most metrics for the subject or entry )
-- each sunject will have one or more episod

DROP TABLE IF EXISTS `subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subject` (
  `subject_id` int NOT NULL AUTO_INCREMENT,
  `address` varchar(255) DEFAULT NULL,
  `patient_admitting_physician` int DEFAULT NULL,
  `allergies` varchar(1024) DEFAULT NULL,
  `assessment_plan` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `creating_user_id` int DEFAULT NULL,
  `created_date` datetime(6) DEFAULT NULL,
  `birth_date` datetime(6) DEFAULT NULL,
  `death_date` datetime(6) DEFAULT NULL,
  `death_indicator` bit(1) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `ethnicity` varchar(255) DEFAULT NULL,
  `forename` varchar(255) DEFAULT NULL,
  `fullname` varchar(255) DEFAULT NULL,
  `gp_email` varchar(255) DEFAULT NULL,
  `gp_fax` varchar(255) DEFAULT NULL,
  `gp_forename` varchar(255) DEFAULT NULL,
  `gp_gmp_code` varchar(255) DEFAULT NULL,
  `gp_pct_code` varchar(255) DEFAULT NULL,
  `gp_pct_name` varchar(255) DEFAULT NULL,
  `gp_postcode` varchar(255) DEFAULT NULL,
  `gp_practice_code` varchar(255) DEFAULT NULL,
  `gp_practice_name` varchar(255) DEFAULT NULL,
  `gp_address` varchar(255) DEFAULT NULL,
  `gp_surname` varchar(255) DEFAULT NULL,
  `gp_phone` varchar(255) DEFAULT NULL,
  `guid` varchar(255) NOT NULL,
  `home_phone` varchar(255) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `language` varchar(255) DEFAULT NULL,
  `marital_status` varchar(255) DEFAULT NULL,
  `middle_name` varchar(255) DEFAULT NULL,
  `mobile_phone` varchar(255) DEFAULT NULL,
  `modified_date` datetime(6) DEFAULT NULL,
  `nationality` varchar(255) DEFAULT NULL,
  `nhs_number` varchar(255) DEFAULT NULL,
  `nok_address` varchar(255) DEFAULT NULL,
  `nok_country` varchar(255) DEFAULT NULL,
  `nok_frename` varchar(255) DEFAULT NULL,
  `nok_postcode` varchar(255) DEFAULT NULL,
  `nok_relationship` varchar(255) DEFAULT NULL,
  `nok_surname` varchar(255) DEFAULT NULL,
  `nok_phone_1` varchar(255) DEFAULT NULL,
  `nok_phone_2` varchar(255) DEFAULT NULL,
  `occupation` varchar(255) DEFAULT NULL,
  `overseas_visitor` varchar(255) DEFAULT NULL,
  `postcode` varchar(255) DEFAULT NULL,
  `priority` int NOT NULL,
  `is_disabled` varchar(255) DEFAULT NULL,
  `religion` varchar(255) DEFAULT NULL,
  `sex` varchar(7) DEFAULT NULL,
  `surname` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `work_phone` varchar(255) DEFAULT NULL,
  `user_user_id` int DEFAULT NULL,
  PRIMARY KEY (`subject_id`),
  UNIQUE KEY `UK1ik70fb2g0sx5b5fnfetr7953` (`guid`),
  UNIQUE KEY `UKrv38gmpn4sr6lvbc2ep4vcmn4` (`user_user_id`),
  CONSTRAINT `FKk2yiicw6j2lns80u3m6nqnt9r` FOREIGN KEY (`user_user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subject`
--

LOCK TABLES `subject` WRITE;
/*!40000 ALTER TABLE `subject` DISABLE KEYS */;
/*!40000 ALTER TABLE `subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subject_notes`
-- not used

DROP TABLE IF EXISTS `subject_notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subject_notes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `note_type` int NOT NULL,
  `notes` varchar(4000) DEFAULT NULL,
  `subject_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UKtq42h7r8baw8phwsvl5l71vag` (`note_type`,`subject_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subject_notes`
--

LOCK TABLES `subject_notes` WRITE;
/*!40000 ALTER TABLE `subject_notes` DISABLE KEYS */;
/*!40000 ALTER TABLE `subject_notes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `summary`
-- Used to generate a summary of forms entered for a subject.
-- The summary can include selected form definitions and their corresponding selected fields.
-- The result will contain all selected fields from the subject's form data.

DROP TABLE IF EXISTS `summary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `summary` (
  `id` int NOT NULL AUTO_INCREMENT,
  `backgroundColor` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `guid` varchar(255) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `createdBy_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UKrdj09qe4hb2yioonbqnn1914e` (`guid`),
  KEY `FKi24kh8l3hp28e3vaqg5kgrkme` (`createdBy_id`),
  CONSTRAINT `FKi24kh8l3hp28e3vaqg5kgrkme` FOREIGN KEY (`createdBy_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `summary`

LOCK TABLES `summary` WRITE;
/*!40000 ALTER TABLE `summary` DISABLE KEYS */;
/*!40000 ALTER TABLE `summary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `summary_field`
-- holds the selected fields in each summary_form

DROP TABLE IF EXISTS `summary_field`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `summary_field` (
  `id` int NOT NULL AUTO_INCREMENT,
  `field_name` varchar(255) DEFAULT NULL,
  `sfield_id` int DEFAULT NULL,
  `item_index` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FKp1qrehg3fog1o71yt9v9wfupg` (`sfield_id`),
  CONSTRAINT `FKp1qrehg3fog1o71yt9v9wfupg` FOREIGN KEY (`sfield_id`) REFERENCES `summary_form` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `summary_field`
--

LOCK TABLES `summary_field` WRITE;
/*!40000 ALTER TABLE `summary_field` DISABLE KEYS */;
/*!40000 ALTER TABLE `summary_field` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `summary_form`
--
-- holds the selected forms in the subject summary
DROP TABLE IF EXISTS `summary_form`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `summary_form` (
  `id` int NOT NULL AUTO_INCREMENT,
  `afobject_id` int DEFAULT NULL,
  `summary_id` int DEFAULT NULL,
  `item_index` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FKljyjilbh6ceb7cw91s4tcry06` (`summary_id`),
  CONSTRAINT `FKljyjilbh6ceb7cw91s4tcry06` FOREIGN KEY (`summary_id`) REFERENCES `summary` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `summary_form`
--

LOCK TABLES `summary_form` WRITE;
/*!40000 ALTER TABLE `summary_form` DISABLE KEYS */;
/*!40000 ALTER TABLE `summary_form` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supporting_staff`
-- A senior staff member has a list of users (supporting staff)
-- they manage or oversee.
-- both  senior staff and supporting staff are entries in users table

DROP TABLE IF EXISTS `supporting_staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `supporting_staff` (
  `senior_staff_id` int NOT NULL,
  `supporting_staff_id` int NOT NULL,
  PRIMARY KEY (`senior_staff_id`,`supporting_staff_id`),
  KEY `FKflimk1s9hq02b9ldyva6wxy5d` (`supporting_staff_id`),
  CONSTRAINT `FKflimk1s9hq02b9ldyva6wxy5d` FOREIGN KEY (`supporting_staff_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `FKitgaevmutoheucphatcvyj0nj` FOREIGN KEY (`senior_staff_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supporting_staff`
--

LOCK TABLES `supporting_staff` WRITE;
/*!40000 ALTER TABLE `supporting_staff` DISABLE KEYS */;
/*!40000 ALTER TABLE `supporting_staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_option_keyvalue`
--

DROP TABLE IF EXISTS `system_option_keyvalue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_option_keyvalue` (
  `id` int NOT NULL AUTO_INCREMENT,
  `isActive` bit(1) NOT NULL,
  `description` varchar(50) DEFAULT NULL,
  `isEnabled` bit(1) NOT NULL,
  `FlagLevel` varchar(255) DEFAULT NULL,
  `system_key` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UKfcd7hfyqod1dhnxjyj9gc6ot7` (`system_key`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_option_keyvalue`
-- Supports multiple types of messaging options such as inbox, email, pager, and SMS.
-- Notifications are sent based on the user's preferred messaging option, which is customizable per user.

LOCK TABLES `system_option_keyvalue` WRITE;
/*!40000 ALTER TABLE `system_option_keyvalue` DISABLE KEYS */;
INSERT INTO `system_option_keyvalue` VALUES (1,_binary '','Notify when Comment is made',_binary '',NULL,'COMMENT_MADE'),(2,_binary '','Response sent to referrer',_binary '',NULL,'RESPONSE_SENT'),(3,_binary '','Image Transfer Failure',_binary '',NULL,'IMAGE_TRANSFER_FAILED'),(4,_binary '','Image Transfer Delayed',_binary '',NULL,'IMAGE_TRANSFER_DELAYED'),(5,_binary '','Image has arrived',_binary '',NULL,'IMAGE_ARRIVED'),(6,_binary '','Reminder to acknowledge response',_binary '',NULL,'REMINDER_ACK_RESPONSE'),(7,_binary '','Patient Response Reminder',_binary '',NULL,'PAT_RESP_REMINDER'),(8,_binary '','Patient Information Amended',_binary '',NULL,'PAT_INFO_AMENDED'),(9,_binary '','Referral Acknowledgement',_binary '',NULL,'REFERRAL_ACK'),(10,_binary '','Patient Referred',_binary '',NULL,'PATIENT_REFERRED'),(11,_binary '','Notification Report',_binary '',NULL,'NOTIFICATION_REPORT'),(12,_binary '','Reminder to respond to referrer',_binary '',NULL,'REFERAL_REMINDER_SEND_RESPONSE'),(13,_binary '','New Patient Arrival',_binary '',NULL,'NEW_PATIENT_ARRIVAL'),(14,_binary '','Response for Patient arrived',_binary '',NULL,'RESPONSE_FOR_PATIENT_ARRIVED'),(15,_binary '','Email Notification',_binary '','GLOBAL','EMAIL'),(16,_binary '','SMS Notification',_binary '','GLOBAL','SMS'),(17,_binary '','Pager Notification',_binary '','GLOBAL','PAGER'),(18,_binary '','Inbox Notification',_binary '','GLOBAL','INBOX');
/*!40000 ALTER TABLE `system_option_keyvalue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_roles`
-- maps users and roles

DROP TABLE IF EXISTS `user_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_roles` (
  `user_id` int NOT NULL,
  `role_id` int NOT NULL,
  KEY `FKh8ciramu9cc9q3qcqiv4ue8a6` (`role_id`),
  KEY `FKhfh9dx7w3ubf1co1vdev94g3f` (`user_id`),
  CONSTRAINT `FKh8ciramu9cc9q3qcqiv4ue8a6` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`),
  CONSTRAINT `FKhfh9dx7w3ubf1co1vdev94g3f` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_roles`
--

LOCK TABLES `user_roles` WRITE;
/*!40000 ALTER TABLE `user_roles` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_speciality`
-- not used
DROP TABLE IF EXISTS `user_speciality`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_speciality` (
  `id` int NOT NULL AUTO_INCREMENT,
  `speciality_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_speciality`
--

LOCK TABLES `user_speciality` WRITE;
/*!40000 ALTER TABLE `user_speciality` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_speciality` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
-- Represents users of the application.
-- Each user has one or more roles and belongs to an organization.
-- Users can log in and have permissions to create  or act on subjects

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `accountNonExpired` bit(1) NOT NULL,
  `accountNonLocked` bit(1) NOT NULL,
  `user_can_edit` bit(1) DEFAULT b'0',
  `creation_date` datetime(6) DEFAULT NULL,
  `credentialsNonExpired` bit(1) NOT NULL,
  `dateAccountExpires` datetime(6) DEFAULT NULL,
  `datePasswordLastChanged` datetime(6) DEFAULT NULL,
  `deleted` bit(1) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `email_verified` bit(1) NOT NULL,
  `enabled` bit(1) NOT NULL,
  `enforceStrongPassword` bit(1) NOT NULL,
  `external_ldap_user_id` varchar(255) DEFAULT NULL,
  `user_forename` varchar(255) DEFAULT NULL,
  `google_user` bit(1) NOT NULL,
  `guid` varchar(255) NOT NULL,
  `is_subject` bit(1) NOT NULL,
  `ldap_user` bit(1) NOT NULL,
  `user_middlename` varchar(255) DEFAULT NULL,
  `modified_date` datetime(6) DEFAULT NULL,
  `user_nickname` varchar(255) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `passwordCanExpire` bit(1) DEFAULT NULL,
  `user_prefix` varchar(255) DEFAULT NULL,
  `profileImagePath` varchar(255) DEFAULT NULL,
  `secret` varchar(255) NOT NULL,
  `user_suffix` varchar(255) DEFAULT NULL,
  `user_surname` varchar(255) DEFAULT NULL,
  `username` varchar(255) NOT NULL,
  `using2FA` bit(1) NOT NULL,
  `organisation_id` int DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `UKedn1g10a5gi53t1f8m5murd1q` (`guid`),
  UNIQUE KEY `UKd1gc5w2bve8v4rdks8mdrqiye` (`secret`),
  UNIQUE KEY `UKr43af9ap4edm43mmtq01oddj6` (`username`),
  KEY `FKhb3nv5nv0xr3wpuxfsb2jft1s` (`organisation_id`),
  CONSTRAINT `FKhb3nv5nv0xr3wpuxfsb2jft1s` FOREIGN KEY (`organisation_id`) REFERENCES `organisation` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-13  9:49:55
