-- MySQL dump 10.13  Distrib 8.4.0, for Win64 (x86_64)
--
-- Host: localhost    Database: tiktok
-- ------------------------------------------------------
-- Server version	8.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actions`
--

DROP TABLE IF EXISTS `actions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `unique_id` varchar(255) NOT NULL,
  `action_type` varchar(255) NOT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=454 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bloggers`
--

DROP TABLE IF EXISTS `bloggers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bloggers` (
  `blogger_id` int NOT NULL AUTO_INCREMENT,
  `blogger_name` varchar(255) NOT NULL,
  PRIMARY KEY (`blogger_id`),
  UNIQUE KEY `blogger_name` (`blogger_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `关注关系`
--

DROP TABLE IF EXISTS `关注关系`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `关注关系` (
  `关注关系ID` int NOT NULL AUTO_INCREMENT,
  `用户ID_关注` int DEFAULT NULL,
  `用户ID_被关注` int DEFAULT NULL,
  `关注时间` datetime DEFAULT NULL,
  PRIMARY KEY (`关注关系ID`),
  UNIQUE KEY `unique_follower_followed` (`用户ID_关注`,`用户ID_被关注`),
  KEY `用户ID_被关注` (`用户ID_被关注`),
  CONSTRAINT `follows_ibfk_1` FOREIGN KEY (`用户ID_关注`) REFERENCES `用户` (`用户ID`),
  CONSTRAINT `follows_ibfk_2` FOREIGN KEY (`用户ID_被关注`) REFERENCES `用户` (`用户ID`)
) ENGINE=InnoDB AUTO_INCREMENT=81531 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `用户`
--

DROP TABLE IF EXISTS `用户`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `用户` (
  `用户ID` int NOT NULL AUTO_INCREMENT,
  `唯一ID` varchar(255) NOT NULL,
  `用户名` varchar(255) DEFAULT NULL,
  `用户类型` set('博主','粉丝') DEFAULT NULL,
  `最后抓取时间` datetime DEFAULT NULL,
  `粉丝数量` int DEFAULT NULL,
  `关注数量` int DEFAULT NULL,
  PRIMARY KEY (`用户ID`),
  UNIQUE KEY `唯一ID` (`唯一ID`)
) ENGINE=InnoDB AUTO_INCREMENT=163079 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-11 14:15:11
