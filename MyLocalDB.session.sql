-- 删除现有的表
DROP TABLE IF EXISTS `follows`;
DROP TABLE IF EXISTS `users`;

-- 创建新的 `users` 表，字段名使用中文
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 创建新的 `follows` 表，字段名使用中文
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


--@block
-- 创建新的数据库

USE `tiktok_擦边`;

-- 创建新表结构
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `粉丝` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `唯一ID` varchar(255) NOT NULL,
  `粉丝ID` varchar(255) NOT NULL,
  `是否处理` boolean DEFAULT FALSE,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `关注` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `唯一ID` varchar(255) NOT NULL,
  `关注ID` varchar(255) NOT NULL,
  `是否处理` boolean DEFAULT FALSE,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `视频信息` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `唯一ID` varchar(255) NOT NULL,
  `视频链接` varchar(255) NOT NULL,
  `播放数` int DEFAULT 0,
  `是否处理` boolean DEFAULT FALSE,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `下载视频` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `唯一ID` varchar(255) NOT NULL,
  `视频链接` varchar(255) NOT NULL,
  `是否审核` boolean DEFAULT FALSE,
  `是否下载` boolean DEFAULT FALSE,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--@block
SELECT  * FROM `关注关系`;


--@block 数据清空
USE `tiktok_擦边`;

-- 禁用外键约束
SET FOREIGN_KEY_CHECKS = 0;

-- 清空表数据
TRUNCATE TABLE `用户`;
TRUNCATE TABLE `关注关系`;
TRUNCATE TABLE `视频信息`;
TRUNCATE TABLE `下载视频`;

-- 启用外键约束
SET FOREIGN_KEY_CHECKS = 1;

--@block
SELECT u.*
FROM `用户` u
JOIN `关注关系` r ON u.`用户ID` = r.`关注ID`
JOIN `用户` u2 ON r.`唯一ID` = u2.`用户ID`
WHERE u2.`唯一ID` = 'naoto.hamanaka';

--@block
SELECT 
    f.`唯一ID` AS 用户ID,
    COUNT(f.`关注ID`) AS 关注次数
FROM 
    `关注关系` AS f
JOIN 
    `用户` AS u ON f.`关注ID` = u.`唯一ID`
WHERE 
    u.`用户类型` = '博主'
GROUP BY 
    f.`唯一ID`
HAVING 
    COUNT(f.`关注ID`) > 1
ORDER BY 
    关注次数 DESC;

--@block 添加唯一键
mysqldump -u root -p --default-character-set=utf8mb4 --no-data --databases tiktok_擦边 > db_structure.sql


--@block 查看数据重复情况
SELECT f.`关注ID`, COUNT(*) as duplicate_count
FROM `关注关系` f
JOIN `用户` u ON f.`唯一ID` = u.`用户ID`
WHERE u.`唯一ID` = 'naoto.hamanaka'
GROUP BY f.`关注ID`
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;
