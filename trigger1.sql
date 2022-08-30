
CREATE DATABASE IF NOT EXISTS `Ticker`;

USE `Ticker`;

CREATE USER IF NOT EXISTS `Ticker`@'%' IDENTIFIED BY '92b9a3b730';
GRANT ALL PRIVILEGES ON *.* TO 'Ticker'@'%' IDENTIFIED BY '92b9a3b730';

/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;



DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`rohit`@`192.168.%`*/ /*!50003 TRIGGER `forSetupNotMoreThan1Value` BEFORE INSERT ON  `Ticker`.`ticker_management_setup`
 FOR EACH ROW BEGIN
 
 IF (SELECT count(*) from `Ticker`.`ticker_management_setup`)<>1 THEN
	signal sqlstate '45000' set message_text = 'Unable to insert as value already found';
 END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`aps`@`localhost`*/ /*!50003 TRIGGER ticker_details_AFTER_UPDATE
AFTER UPDATE ON ticker_management_tickerdetails
FOR EACH ROW
BEGIN
	IF OLD.is_deleted = 0 AND NEW.is_deleted = 1 AND OLD.is_active= 1 AND NEW.is_active = 0 THEN
		INSERT into `ticker_management_tickerhistory` (ticker_id,ticker_type,ticker_json,created_by,created_on
			,modified_by,modified_on,is_active,is_deleted,deleted_on,ticker_end_time
			,ticker_start_time,ticker_title,floors,rooms,ticker_priority,wings
			,frequency,occuring_days,rundeckid,roomTypeSelection)
		values(
			NEW.ticker_id,NEW.ticker_type,NEW.ticker_json,NEW.created_by,NEW.created_on
			,NEW.modified_by,NEW.modified_on,NEW.is_active,NEW.is_deleted,NEW.deleted_on,NEW.ticker_end_time
			,NEW.ticker_start_time,NEW.ticker_title,NEW.floors,rooms,NEW.ticker_priority,wings
			,NEW.frequency,NEW.occuring_days,NEW.rundeckid,NEW.roomTypeSelection);
	END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;


--
-- Dumping events for database 'Ticker'
--
/*!50106 SET @save_time_zone= @@TIME_ZONE */ ;
/*!50106 DROP EVENT IF EXISTS `event_ticker_history` */;
DELIMITER ;;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;;
/*!50003 SET character_set_client  = utf8mb4 */ ;;
/*!50003 SET character_set_results = utf8mb4 */ ;;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;;
/*!50003 SET @saved_time_zone      = @@time_zone */ ;;
/*!50003 SET time_zone             = 'SYSTEM' */ ;;
/*!50106 CREATE*/ /*!50117 DEFINER=`aps`@`localhost`*/ /*!50106 EVENT `event_ticker_history` ON SCHEDULE EVERY 1 DAY STARTS '2022-07-26 18:10:47' ON COMPLETION PRESERVE ENABLE DO BEGIN
		DELETE FROM `ticker_management_tickerdetails` WHERE is_deleted = 1;	    
END */ ;;
/*!50003 SET time_zone             = @saved_time_zone */ ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;;
/*!50003 SET character_set_client  = @saved_cs_client */ ;;
/*!50003 SET character_set_results = @saved_cs_results */ ;;
/*!50003 SET collation_connection  = @saved_col_connection */ ;;
DELIMITER ;
/*!50106 SET TIME_ZONE= @save_time_zone */ ;

--
-- Dumping routines for database 'Ticker'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-08-26 12:43:14
