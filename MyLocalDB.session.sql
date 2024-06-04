

--@block
DROP TABLE followers;


--@block
ALTER TABLE Users
MODIFY username VARCHAR(255) NULL;

--@block
CREATE TABLE Follows (
    follow_id INT AUTO_INCREMENT PRIMARY KEY,
    follower_id INT,
    followed_id INT,
    date_followed DATETIME,
    FOREIGN KEY (follower_id) REFERENCES Users(user_id),
    FOREIGN KEY (followed_id) REFERENCES Users(user_id)
);


--@block
SELECT u.unique_id, u.username, COUNT(f.followed_id) as num_followed
FROM Users u
JOIN Follows f ON u.user_id = f.follower_id
GROUP BY u.user_id, u.unique_id, u.username
HAVING COUNT(f.followed_id) > 1
ORDER BY num_followed DESC;

--@block
DESCRIBE Users;
DESCRIBE Follows;
SELECT  * FROM follows;
SELECT * from users;
SELECT * FROM bloggers;

--@block
SELECT DISTINCT u.unique_id AS other_user_unique_id, u.username AS other_username, f2.followed_id AS common_followed_id
FROM Users u
JOIN Follows f1 ON u.user_id = f1.follower_id
JOIN Follows f2 ON f1.followed_id = f2.followed_id
WHERE f2.follower_id = 2
  AND f1.follower_id <> 2;

--@block
SELECT * from bloggers;

ALTER TABLE Users
MODIFY COLUMN user_type SET('blogger', 'follower') NULL;

ALTER TABLE Follows ADD UNIQUE KEY unique_follower_followed (follower_id, followed_id);


--@block
SHOW DATABASES;

USE tiktok;

SHOW TABLES;

ALTER TABLE Users
ADD COLUMN follower_count INT NULL,
ADD COLUMN following_count INT NULL;

