import json
import os
import time
import random
import pyautogui
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '6152434',
    'database': 'tiktok_擦边'
}

def connect_to_database():
    connection = mysql.connector.connect(**db_config)
    return connection

def check_user_permission(cursor, unique_id, list_type):
    if list_type == '关注列表':
        check_query = "SELECT `关注列表` FROM `用户` WHERE `唯一ID` = %s"
    elif list_type == '粉丝列表':
        check_query = "SELECT `粉丝列表` FROM `用户` WHERE `唯一ID` = %s"
    cursor.execute(check_query, (unique_id,))
    result = cursor.fetchone()
    if result:
        return result[0] == '禁止'
    return False

def update_or_insert_user(cursor, user_data):
    unique_id = user_data['uniqueId']
    username = user_data.get('nickname', None)

    check_query = "SELECT `用户ID` FROM `用户` WHERE `唯一ID` = %s"
    cursor.execute(check_query, (unique_id,))
    result = cursor.fetchone()

    if result:
        update_query = """
            UPDATE `用户`
            SET `用户名` = %s,
                `最后抓取时间` = NOW()
            WHERE `唯一ID` = %s
        """
        cursor.execute(update_query, (username, unique_id))
    else:
        insert_query = """
            INSERT INTO `用户` (`唯一ID`, `用户名`, `最后抓取时间`)
            VALUES (%s, %s, NOW())
        """
        cursor.execute(insert_query, (unique_id, username))

def insert_follow_relationship(cursor, follower_unique_id, followed_unique_id):
    insert_query = """
        INSERT INTO `关注关系` (`唯一ID`, `关注ID`, `是否处理`)
        VALUES (%s, %s, FALSE)
        ON DUPLICATE KEY UPDATE `是否处理` = FALSE
    """
    cursor.execute(insert_query, (follower_unique_id, followed_unique_id))
def scroll_list(driver, unique_id, list_type):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        if check_user_permission(cursor, unique_id, list_type):
            print(f"User {unique_id} is prohibited from accessing {list_type}.")
            return

        output_folder = os.path.join(os.getcwd(), list_type)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        output_file_path = os.path.join(output_folder, f'{unique_id}.txt')
        
        list_xpath = '//div[contains(@class, "DivUserListContainer")]'
        user_list = driver.find_element(By.XPATH, list_xpath)
        
        initial_accounts = driver.find_elements(By.XPATH, f'{list_xpath}//li/div/div/a/div/p')
        initial_count = len(initial_accounts)
        print(f"Initial count of accounts: {initial_count}")
        
        if initial_count == 0:
            print("User has restricted access to their follower or following list.")
            if list_type == '关注列表':
                update_query = "UPDATE `用户` SET `关注列表` = '禁止' WHERE `唯一ID` = %s"
            elif list_type == '粉丝列表':
                update_query = "UPDATE `用户` SET `粉丝列表` = '禁止' WHERE `唯一ID` = %s"
            cursor.execute(update_query, (unique_id,))
            connection.commit()
            cursor.close()
            connection.close()
            return
        
        unique_users = set()
        no_new_account_count = 0

        element_location = initial_accounts[2].location
        x, y = element_location['x'], element_location['y']

        pyautogui.moveTo(x + 150, y + 100)
        pyautogui.mouseDown(button='middle')
        time.sleep(0.1)
        pyautogui.mouseUp(button='middle')
        pyautogui.moveTo(x + 150, y + 300)

        with open(output_file_path, 'w', encoding='utf-8') as file:
            while no_new_account_count < 10:
                current_accounts = driver.find_elements(By.XPATH, f'{list_xpath}//li/div/div/a/div/p')
                current_count = len(current_accounts)
                print(f"Current count of accounts: {current_count}")
                
                for user_element in current_accounts:
                    try:
                        user_unique_id = user_element.text
                        if user_unique_id not in unique_users:
                            unique_users.add(user_unique_id)
                            file.write(f"{user_unique_id}\n")

                    except Exception as e:
                        print(f"Error processing user {user_unique_id}: {e}")
                
                if current_count == initial_count:
                    no_new_account_count += 1
                    print(f"No new accounts loaded, attempt {no_new_account_count}.")
                else:
                    no_new_account_count = 0
                    initial_count = current_count
                
                if no_new_account_count >= 10:
                    break

            print("Stopping scroll as no new accounts loaded for ten consecutive attempts.")
            pyautogui.mouseDown(button='middle')
            time.sleep(0.1)
            pyautogui.mouseUp(button='middle')

        if list_type == '关注列表':
            update_query = "UPDATE `用户` SET `关注列表` = '已处理' WHERE `唯一ID` = %s"
        elif list_type == '粉丝列表':
            update_query = "UPDATE `用户` SET `粉丝列表` = '已处理' WHERE `唯一ID` = %s"
        cursor.execute(update_query, (unique_id,))
        
        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        print(f"Error scrolling followers list: {e}")

def load_list(driver, unique_id, list_type):
    profile_url = f'https://www.tiktok.com/@{unique_id}'
    driver.get(profile_url)
    time.sleep(5)
    try:
        if list_type == '关注列表':
            button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div[1]/h3/div[1]/span')
        elif list_type == '粉丝列表':
            button = driver.find_element(By.XPATH, '//strong[@title="粉丝"]')
        
        button.click()
        time.sleep(5)
        scroll_list(driver, unique_id, list_type)
    except Exception as e:
        print(f"Error clicking {list_type} button or scrolling: {e}")

def import_list_to_database(unique_id, list_type):
    connection = connect_to_database()
    cursor = connection.cursor()
    
    output_folder = os.path.join(os.getcwd(), list_type)
    output_file_path = os.path.join(output_folder, f'{unique_id}.txt')

    with open(output_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            user_unique_id = line.strip()
            user_data = {'uniqueId': user_unique_id, 'nickname': user_unique_id}
            update_or_insert_user(cursor, user_data)

            # 插入关注关系时，明确用户与关注者的关系
            if list_type == '关注列表':
                insert_follow_relationship(cursor, unique_id, user_unique_id)
            elif list_type == '粉丝列表':
                insert_follow_relationship(cursor, user_unique_id, unique_id)
    
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    unique_id = 'patriciarodriguez9631'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    action = input("Please provide an action (粉丝列表, 关注列表): ")

    if action == "粉丝列表":
        load_list(driver, unique_id, '粉丝列表')
        import_list_to_database(unique_id, '粉丝列表')
    elif action == "关注列表":
        load_list(driver, unique_id, '关注列表')
        import_list_to_database(unique_id, '关注列表')
    
    driver.quit()
