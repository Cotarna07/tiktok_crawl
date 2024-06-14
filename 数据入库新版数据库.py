import json
import mysql.connector
import os

# 数据库连接配置
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

def process_json_file(json_file):
    print(f"Processing file: {json_file}")
    if not os.path.exists(json_file):
        print(f"The file {json_file} does not exist.")
        return

    with open(json_file, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            print(f"Successfully loaded JSON data from {json_file}")
        except json.JSONDecodeError as err:
            print(f"Error decoding JSON from file {json_file}: {err}")
            return

    if not data:
        print(f"The file {json_file} contains no data.")
        return

    connection = connect_to_database()
    cursor = connection.cursor()

    # 获取博主的uniqueId
    filename = os.path.basename(json_file)
    blogger_unique_id = filename.rsplit('_followers.json', 1)[0]
    
    cursor.execute("SELECT `用户ID` FROM `用户` WHERE `唯一ID` = %s", (blogger_unique_id,))
    blogger_id = cursor.fetchone()
    if not blogger_id:
        # 博主不存在，插入博主数据
        cursor.execute("INSERT INTO `用户` (`唯一ID`, `用户名`, `用户类型`) VALUES (%s, %s, '博主')", (blogger_unique_id, blogger_unique_id))
        blogger_id = cursor.lastrowid
    else:
        blogger_id = blogger_id[0]

    for entry in data:
        user_data = entry.get('user', None)
        stats_data = entry.get('stats', None)
        if user_data and stats_data:
            update_or_insert_user(cursor, user_data, stats_data)
            # 获取粉丝的用户ID
            cursor.execute("SELECT `用户ID` FROM `用户` WHERE `唯一ID` = %s", (user_data['uniqueId'],))
            follower_id = cursor.fetchone()
            if follower_id:
                follower_id = follower_id[0]
                insert_follow_relationship(cursor, user_data['uniqueId'], blogger_unique_id)
            else:
                print(f"Failed to find or insert user: {user_data['uniqueId']}")
        else:
            print(f"Missing 'user' or 'stats' key in entry: {entry}")

    connection.commit()
    cursor.close()
    connection.close()
    print(f"Finished processing file: {json_file}")

def main():
    json_directory = 'D:\\softwear\\TikHubio\\粉丝账号数据json'
    files = [
        "oh_terri_followers.json",
        "paytonsartain_followers.json",
        "princessekaatrin_followers.json",
        "s.catharina__followers.json",
        "saracrumbleleg_followers.json",
        "soophie.schnr_followers.json",
        "angelicalivolti_followers.json",
        "blakehealey1_followers.json",
        "clairerose_followers.json",
        "emmyjanestevens_followers.json",
        "faithult_followers.json",
        "janaeerobertss_followers.json",
        "jourdansloane_followers.json",
        "loummartines_followers.json",
        "maddiefrancesssca_followers.json",
        "masonanneoglesby_followers.json",
        "neverbaby26_followers.json",
        "notbellla__followers.json"
    ]

    for file in files:
        process_json_file(os.path.join(json_directory, file))

if __name__ == "__main__":
    main()
