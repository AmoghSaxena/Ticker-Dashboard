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
-- Table structure for table `ticker_management_setup`
--

DROP TABLE IF EXISTS `ticker_management_setup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ticker_management_setup` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `FQDN` varchar(60) NOT NULL,
  `Dvs_Token` varchar(150) DEFAULT NULL,
  `Rundeck_Token` varchar(150) DEFAULT NULL,
  `Apache_server_url` varchar(150) DEFAULT NULL,
  `Ticker_FQDN` varchar(150) DEFAULT NULL,
  `Rundeck_Api_Version` int(11) NOT NULL,
  `Rundeck_Start_Job` varchar(150) DEFAULT NULL,
  `Rundeck_Stop_Job` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticker_management_setup`
--

LOCK TABLES `ticker_management_setup` WRITE;
/*!40000 ALTER TABLE `ticker_management_setup` DISABLE KEYS */;
INSERT INTO `ticker_management_setup` VALUES (1,'dvs-uatblue.digivalet.com','da1ca0a34d72bd530bfc21b7a4d70ec903a0611c18058eb8b6290cae6644251e','GPE0a5rF328fUHV9Zwj1kmQSudVY0zOn','https://media.ticker.dns.army','ticker.dns.army',17,'0d0c3cfe-adcd-4f86-8c03-adaa1cd2c0e0','ba459f2d-47be-4dc6-98eb-546ceca3f62a');
/*!40000 ALTER TABLE `ticker_management_setup` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-08-03 11:15:31
