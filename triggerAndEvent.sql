-- MySQL dump 10.19  Distrib 10.3.34-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: Ticker
-- ------------------------------------------------------
-- Server version	10.3.34-MariaDB-0ubuntu0.20.04.1
USE `Ticker`;

DROP TRIGGER IF EXISTS `forSetupNotMoreThan1Value`;

DELIMITER ;;
/*!50003 CREATE*//*!50003 TRIGGER `forSetupNotMoreThan1Value` BEFORE INSERT ON  `Ticker`.`ticker_management_setup`
 FOR EACH ROW BEGIN
 
 IF (SELECT count(*) from `Ticker`.`ticker_management_setup`)<>1 THEN
	signal sqlstate '45000' set message_text = 'Unable to insert as value already found';
 END IF;
END */;;
DELIMITER ;

DROP TRIGGER IF EXISTS `ticker_details_AFTER_UPDATE`;

DELIMITER ;;
/*!50003 CREATE*/ /*!50003 TRIGGER ticker_details_AFTER_UPDATE
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


/*!50106 DROP EVENT IF EXISTS `event_ticker_history` */;
DELIMITER ;;

/*!50106 CREATE*//*!50106 EVENT `event_ticker_history` ON SCHEDULE EVERY 1 DAY STARTS '2022-07-26 18:10:47' ON COMPLETION PRESERVE ENABLE DO BEGIN
		DELETE FROM `ticker_management_tickerdetails` WHERE is_deleted = 1;	    
END */ ;;

DELIMITER ;



-- Dump completed on 2022-09-15 15:06:45
