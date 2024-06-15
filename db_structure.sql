-- Table: 下载视频
CREATE TABLE `下载视频` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `唯一ID` varchar(255) NOT NULL,
  `视频链接` varchar(255) NOT NULL,
  `是否审核` tinyint(1) DEFAULT '0',
  `是否下载` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table: 关注关系
CREATE TABLE `关注关系` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `唯一ID` varchar(255) NOT NULL,
  `关注ID` varchar(255) NOT NULL,
  `是否处理` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `unique_follow_relationship` (`唯一ID`,`关注ID`)
) ENGINE=InnoDB AUTO_INCREMENT=94891 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table: 用户
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
) ENGINE=InnoDB AUTO_INCREMENT=93489 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table: 视频信息
CREATE TABLE `视频信息` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `唯一ID` varchar(255) NOT NULL,
  `视频链接` varchar(255) NOT NULL,
  `播放数` int DEFAULT '0',
  `是否处理` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `unique_video_link` (`唯一ID`,`视频链接`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

