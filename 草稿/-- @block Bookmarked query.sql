-- @block Bookmarked query
-- @group Ungrouped
-- @name 001

--@block
USE tiktok_擦边;
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
