-- MySQL dump 10.19  Distrib 10.3.34-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: Ticker
-- ------------------------------------------------------
-- Server version	10.3.34-MariaDB-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ticker_management_tickerdetails`
--

DROP TABLE IF EXISTS `ticker_management_tickerdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ticker_management_tickerdetails` (
  `ticker_id` int(11) NOT NULL AUTO_INCREMENT,
  `ticker_type` varchar(60) NOT NULL,
  `ticker_json` longtext NOT NULL,
  `wings` varchar(300) DEFAULT NULL,
  `created_by` varchar(50) DEFAULT NULL,
  `created_on` datetime(6) NOT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `modified_on` datetime(6) NOT NULL,
  `is_active` int(10) unsigned NOT NULL CHECK (`is_active` >= 0),
  `is_deleted` int(10) unsigned NOT NULL CHECK (`is_deleted` >= 0),
  `deleted_on` datetime(6) DEFAULT NULL,
  `ticker_end_time` datetime(6) DEFAULT NULL,
  `ticker_start_time` datetime(6) DEFAULT NULL,
  `ticker_title` varchar(50) NOT NULL,
  `floors` varchar(300) DEFAULT NULL,
  `rooms` varchar(300) DEFAULT NULL,
  `ticker_priority` varchar(10) NOT NULL,
  `frequency` varchar(30) DEFAULT NULL,
  `occuring_days` varchar(500) DEFAULT NULL,
  `roomTypeSelection` varchar(300) DEFAULT NULL,
  `rundeck_id` int(11) DEFAULT NULL,
  `rundeckid` int(10) unsigned DEFAULT NULL CHECK (`rundeckid` >= 0),
  PRIMARY KEY (`ticker_id`)
) ENGINE=InnoDB AUTO_INCREMENT=353 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticker_management_tickerdetails`
--
-- WHERE:  ticker_id=352

LOCK TABLES `ticker_management_tickerdetails` WRITE;
/*!40000 ALTER TABLE `ticker_management_tickerdetails` DISABLE KEYS */;
INSERT INTO `ticker_management_tickerdetails` VALUES (352,'Scrolling Ticker','{\n   \"static_ticker_condition\": false,\n   \"main_ticker_condition\": true,\n   \"moving_ticker_condition\": false,\n   \"optional_ticker_condition\": false,\n   \"emergency_ticker_condition\": false,\n   \"time_interval\": 60,\n   \"main_ticker_position\": \"down\",\n   \"main_ticker_message\": \"Bhagwan ka diya hua Sabkuch hai.. Daulath hai, Shohrat hai Izzat hai Izzat Hai? Izzat Hai? Ha hai.. thodi bohot\",\n   \"main_ticker_logo\": false,\n   \"main_ticker_font\": \"TimesNewRoman\",\n   \"main_ticker_font_size\": \"x-large\",\n   \"main_ticker_bgcolor\": [\n      255,\n      50,\n      50\n   ],\n   \"main_ticker_font_color\": [\n      247,\n      249,\n      249\n   ],\n   \"main_ticker_speed\": \"normal\",\n   \"main_ticker_motion\": \"right-left\",\n   \"ticker_type\": \"Scrolling Ticker\",\n   \"ticker_id\": 352\n}','[\'Wing A\']','admin','2022-07-21 16:45:10.554816','admin','2022-07-21 16:45:10.554856',0,1,NULL,'2022-07-21 16:59:00.000000','2022-07-21 16:46:00.000000','Scrolling Ticker','[\'1st Floor\']','[\'1274\']','Medium','5 minutes','Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday','[\'Standard\']',NULL,6759);
/*!40000 ALTER TABLE `ticker_management_tickerdetails` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-07-21 18:01:26
