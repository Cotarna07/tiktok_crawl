import mysql.connector

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '6152434',
    'database': 'tiktok_擦边'
}

def check_following_count(unique_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    query = """
    SELECT COUNT(*) AS `关注的博主数量`
    FROM `关注关系`
    WHERE `唯一ID` = (
        SELECT `用户ID` FROM `用户` WHERE `唯一ID` = %s
    );
    """
    cursor.execute(query, (unique_id,))
    result = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    return result[0]

if __name__ == "__main__":
    unique_id = 'heavenmayhem'
    count = check_following_count(unique_id)
    print(f"{unique_id} 关注的博主数量: {count}")
