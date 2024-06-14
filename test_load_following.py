import json
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
import random
import os
import pyautogui

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

def scroll_followers_list(driver, unique_id):
    try:
        # 创建“关注列表”文件夹（如果不存在）
        output_folder = os.path.join(os.getcwd(), '关注列表')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # 设置输出文件路径
        output_file_path = os.path.join(output_folder, f'{unique_id}.txt')
        
        followers_list_xpath = '//div[contains(@class, "DivUserListContainer")]'
        followers_list = driver.find_element(By.XPATH, followers_list_xpath)
        
        initial_accounts = driver.find_elements(By.XPATH, f'{followers_list_xpath}//li/div/div/a/div/p')
        initial_count = len(initial_accounts)
        print(f"Initial count of accounts: {initial_count}")
        
        unique_users = set()
        
        no_new_account_count = 0

        # 获取初始账号位置
        element_location = initial_accounts[2].location
        x, y = element_location['x'], element_location['y']

        # 使用 pyautogui 移动鼠标并模拟中键点击
        pyautogui.moveTo(x+300, y+50)
        pyautogui.mouseDown(button='middle')
        time.sleep(0.1)  # 等待加载
        pyautogui.mouseUp(button='middle')
        pyautogui.moveTo(x+300, y + 250)

        with open(output_file_path, 'w', encoding='utf-8') as file:
            while no_new_account_count < 40:

                current_accounts = driver.find_elements(By.XPATH, f'{followers_list_xpath}//li/div/div/a/div/p')
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
                
                # 如果检测到20次滚动没有新用户，提前退出循环
                if no_new_account_count >= 40:
                    break

            print("Stopping scroll as no new accounts loaded for twenty consecutive attempts.")
        
    except Exception as e:
        print(f"Error scrolling followers list: {e}")
def load_following(driver, unique_id):
    profile_url = f'https://www.tiktok.com/@{unique_id}'
    driver.get(profile_url)
    time.sleep(5)
    try:
        following_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div[1]/h3/div[1]/span')
        following_button.click()
        time.sleep(5)
        
        scroll_followers_list(driver, unique_id)
        
    except Exception as e:
        print(f"Error clicking following button or scrolling: {e}")

# def load_cookies(driver, cookie_file):
#     with open(cookie_file, 'r', encoding='utf-8') as file:
#         cookies = json.load(file)
#     for cookie in cookies:
#         driver.add_cookie(cookie)

def start_chrome_browser():
    subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--remote-debugging-port=9222"])
    time.sleep(5)

    options = ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=options)
    return driver

def import_followers_to_database(unique_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    
    output_folder = os.path.join(os.getcwd(), '关注列表')
    output_file_path = os.path.join(output_folder, f'{unique_id}.txt')

    with open(output_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            user_unique_id = line.strip()
            user_data = {'uniqueId': user_unique_id, 'nickname': user_unique_id}
            update_or_insert_user(cursor, user_data)

            cursor.execute("SELECT `用户ID` FROM `用户` WHERE `唯一ID` = %s", (unique_id,))
            naoto_id = cursor.fetchone()[0]

            cursor.execute("SELECT `用户ID` FROM `用户` WHERE `唯一ID` = %s", (user_unique_id,))
            followed_id = cursor.fetchone()[0]

            insert_follow_relationship(cursor, naoto_id, followed_id)
    
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    driver = start_chrome_browser()
    # driver.get("https://www.tiktok.com")
    # time.sleep(5)
    
    # cookie_file = "D:/software/tiktok_crawl/config.json"
    # load_cookies(driver, cookie_file)
    # time.sleep(5)
    
    unique_id = "heavenmayhem"
    load_following(driver, unique_id)
    
    import_followers_to_database(unique_id)
    
    driver.quit()
