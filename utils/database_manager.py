import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '6152434',
    'database': 'tiktok_擦边'
}

def connect_to_database():
    print("Connecting to database...")
    connection = mysql.connector.connect(**db_config)
    print("Connected to database")
    return connection

def update_or_insert_user(cursor, user_data, stats_data):
    unique_id = user_data['uniqueId']
    username = user_data.get('nickname', None)
    follower_count = stats_data.get('followerCount', None)
    following_count = stats_data.get('followingCount', None)

    # 检查用户是否已经存在
    check_query = "SELECT `用户ID` FROM `用户` WHERE `唯一ID` = %s"
    cursor.execute(check_query, (unique_id,))
    result = cursor.fetchone()

    if result:
        # 用户已存在，更新数据
        update_query = """
            UPDATE `用户`
            SET `用户名` = %s,
                `粉丝数量` = %s,
                `关注数量` = %s,
                `最后抓取时间` = NOW()
            WHERE `唯一ID` = %s
        """
        cursor.execute(update_query, (username, follower_count, following_count, unique_id))
    else:
        # 用户不存在，插入新数据
        insert_query = """
            INSERT INTO `用户` (`唯一ID`, `用户名`, `粉丝数量`, `关注数量`, `最后抓取时间`)
            VALUES (%s, %s, %s, %s, NOW())
        """
        cursor.execute(insert_query, (unique_id, username, follower_count, following_count))

def insert_follow_relationship(cursor, follower_id, followed_id):
    # 插入关注关系
    insert_query = """
        INSERT INTO `关注关系` (`唯一ID`, `关注ID`, `是否处理`)
        VALUES (%s, %s, FALSE)
        ON DUPLICATE KEY UPDATE `是否处理` = FALSE
    """
    cursor.execute(insert_query, (follower_id, followed_id))

def save_video_data(unique_id, video_data):
    connection = connect_to_database()
    cursor = connection.cursor()
    for video in video_data:
        insert_query = """
            INSERT INTO `视频` (`唯一ID`, `视频链接`, `播放量`)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (unique_id, video['url'], video['play_count']))
    connection.commit()
    cursor.close()
    connection.close()
