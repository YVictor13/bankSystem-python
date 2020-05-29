/*
SQLyog Ultimate v12.09 (64 bit)
MySQL - 8.0.19 : Database - banksystem
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`banksystem` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `banksystem`;

/*Table structure for table `card` */

DROP TABLE IF EXISTS `card`;

CREATE TABLE `card` (
  `CardId` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `password` varchar(32) NOT NULL,
  `money` varchar(20) DEFAULT NULL,
  `accountId` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`CardId`),
  KEY `accountId` (`accountId`),
  CONSTRAINT `card_ibfk_1` FOREIGN KEY (`accountId`) REFERENCES `user` (`accountId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `card` */

insert  into `card`(`CardId`,`name`,`password`,`money`,`accountId`) values (1,'1','1','100','1');

/*Table structure for table `deposit` */

DROP TABLE IF EXISTS `deposit`;

CREATE TABLE `deposit` (
  `id` int NOT NULL AUTO_INCREMENT,
  `accountId` varchar(64) DEFAULT NULL,
  `CardId` int DEFAULT NULL,
  `datetime` datetime NOT NULL,
  `money` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `accountId` (`accountId`),
  KEY `CardId` (`CardId`),
  CONSTRAINT `deposit_ibfk_1` FOREIGN KEY (`accountId`) REFERENCES `user` (`accountId`),
  CONSTRAINT `deposit_ibfk_2` FOREIGN KEY (`CardId`) REFERENCES `card` (`CardId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `deposit` */

insert  into `deposit`(`id`,`accountId`,`CardId`,`datetime`,`money`) values (1,'1',1,'2020-05-29 15:39:36','100');

/*Table structure for table `transfer` */

DROP TABLE IF EXISTS `transfer`;

CREATE TABLE `transfer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `accountId` varchar(64) DEFAULT NULL,
  `my_CardId` int DEFAULT NULL,
  `other_CardId` int DEFAULT NULL,
  `datetime` datetime NOT NULL,
  `money` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `accountId` (`accountId`),
  KEY `my_CardId` (`my_CardId`),
  KEY `other_CardId` (`other_CardId`),
  CONSTRAINT `transfer_ibfk_1` FOREIGN KEY (`accountId`) REFERENCES `user` (`accountId`),
  CONSTRAINT `transfer_ibfk_2` FOREIGN KEY (`my_CardId`) REFERENCES `card` (`CardId`),
  CONSTRAINT `transfer_ibfk_3` FOREIGN KEY (`other_CardId`) REFERENCES `card` (`CardId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `transfer` */

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `accountId` varchar(64) DEFAULT NULL,
  `email` varchar(128) NOT NULL,
  `password` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `accountId` (`accountId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `user` */

insert  into `user`(`id`,`accountId`,`email`,`password`) values (1,'1','1@qq.com','1');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
