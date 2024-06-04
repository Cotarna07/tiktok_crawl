import json
import mysql.connector
import os

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '6152434',
    'database': 'tiktok'
}

def connect_to_database():
    print("Connecting to database...")
    connection = mysql.connector.connect(**db_config)
    print("Connected to database")
    return connection

def update_user_counts(cursor, user_data, stats_data):
    unique_id = user_data['uniqueId']
    follower_count = stats_data.get('followerCount', None)
    following_count = stats_data.get('followingCount', None)
    
    print(f"User Data: {user_data}")  # 打印用户数据进行调试
    print(f"Stats Data: {stats_data}")  # 打印统计数据进行调试
    
    update_query = """
        UPDATE Users
        SET follower_count = %s,
            following_count = %s,
            last_crawled = NOW()
        WHERE unique_id = %s
    """
    try:
        print(f"Updating user: {unique_id} with follower_count: {follower_count} and following_count: {following_count}")
        cursor.execute(update_query, (follower_count, following_count, unique_id))
        print(f"Successfully updated user: {unique_id}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print(f"Failed to update user: {unique_id} with follower_count: {follower_count} and following_count: {following_count}")

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

    for entry in data:
        user_data = entry.get('user', None)
        stats_data = entry.get('stats', None)
        if user_data and stats_data:
            update_user_counts(cursor, user_data, stats_data)
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