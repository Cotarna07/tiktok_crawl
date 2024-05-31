import mysql.connector

def connect_to_database():
    connection = mysql.connector.connect(
        host='localhost',  # 替换为您的数据库主机
        user='root',  # 替换为您的数据库用户名
        password='6152434',  # 替换为您的数据库密码
        database='tiktok'  # 替换为您的数据库名称
    )
    return connection

def save_follower_data(unique_id, followers_data):
    connection = connect_to_database()
    cursor = connection.cursor()

    for follower in followers_data:
        cursor.execute("INSERT INTO followers (unique_id, follower_url) VALUES (%s, %s)", (unique_id, follower))
    
    connection.commit()
    cursor.close()
    connection.close()

def save_video_data(unique_id, video_data):
    connection = connect_to_database()
    cursor = connection.cursor()

    for video in video_data:
        cursor.execute("INSERT INTO videos (unique_id, video_url, play_count) VALUES (%s, %s, %s)", 
                       (unique_id, video['url'], video['play_count']))
    
    connection.commit()
    cursor.close()
    connection.close()

def check_action_done(unique_id, action_type):
    connection = connect_to_database()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM actions WHERE unique_id = %s AND action_type = %s", (unique_id, action_type))
    result = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    return result is not None

def save_action_done(unique_id, action_type):
    connection = connect_to_database()
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO actions (unique_id, action_type) VALUES (%s, %s)", (unique_id, action_type))
    
    connection.commit()
    cursor.close()
    connection.close()
