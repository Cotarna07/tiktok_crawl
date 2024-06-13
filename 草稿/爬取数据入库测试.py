import json
import time
import subprocess
from test_cookie_manager import load_cookies, update_browser_cookies, save_last_processed_user, load_last_processed_user, save_cookies, validate_cookies
from test_browser_scheduler import start_chrome_browser, start_edge_browser, start_firefox_browser
from actions.download_videos import download_top_videos
from database_manager import check_action_done, save_action_done
from random_actions import perform_random_actions
from actions.load_followers import load_followers
from actions import load_videos
from selenium.webdriver.common.by import By
import mysql.connector

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

def insert_user(cursor, unique_id, username, user_type):
    check_query = "SELECT `用户ID` FROM `用户` WHERE `唯一ID` = %s"
    cursor.execute(check_query, (unique_id,))
    result = cursor.fetchone()

    if not result:
        insert_query = """
            INSERT INTO `用户` (`唯一ID`, `用户名`, `用户类型`, `最后抓取时间`)
            VALUES (%s, %s, %s, NOW())
        """
        cursor.execute(insert_query, (unique_id, username, user_type))

def insert_follow_relationship(cursor, follower_unique_id, followed_unique_id):
    follower_query = "SELECT `用户ID` FROM `用户` WHERE `唯一ID` = %s"
    followed_query = "SELECT `用户ID` FROM `用户` WHERE `唯一ID` = %s"

    cursor.execute(follower_query, (follower_unique_id,))
    follower_id = cursor.fetchone()
    cursor.execute(followed_query, (followed_unique_id,))
    followed_id = cursor.fetchone()

    if follower_id and followed_id:
        insert_query = """
            INSERT INTO `关注关系` (`用户ID_关注`, `用户ID_被关注`, `关注时间`)
            VALUES (%s, %s, NOW())
            ON DUPLICATE KEY UPDATE `关注时间` = NOW()
        """
        cursor.execute(insert_query, (follower_id[0], followed_id[0]))

def load_followings(driver, unique_id):
    profile_url = f'https://www.tiktok.com/@{unique_id}'
    driver.get(profile_url)
    time.sleep(5)

    followings_button = driver.find_element(By.XPATH, '//span[@data-e2e="following"]')
    followings_button.click()
    time.sleep(5)

    followings_list_xpath = '//div[contains(@class, "DivUserListContainer")]'
    followings_list = driver.find_element(By.XPATH, followings_list_xpath)

    scroll_pause_time = 2
    last_height = driver.execute_script("return arguments[0].scrollHeight", followings_list)

    while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followings_list)
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return arguments[0].scrollHeight", followings_list)
        if new_height == last_height:
            break
        last_height = new_height

    followings = driver.find_elements(By.XPATH, f'{followings_list_xpath}//a[@class="es616eb3 css-5c23qb-StyledLink-StyledUserInfoLink er1vbsz0"]')

    connection = connect_to_database()
    cursor = connection.cursor()

    for following in followings:
        following_unique_id = following.get_attribute('href').split('/')[-1]
        following_username = following.text
        insert_user(cursor, following_unique_id, following_username, '粉丝')
        insert_follow_relationship(cursor, unique_id, following_unique_id)

    connection.commit()
    cursor.close()
    connection.close()
    print(f"Successfully loaded and stored followings for user: {unique_id}")

def get_user_unique_ids(json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return [user['user']['uniqueId'] for user in data]
    except Exception as e:
        print(f"Error loading user unique IDs: {e}")
        return []

def process_user(driver, unique_id, action):
    profile_url = f'https://www.tiktok.com/@{unique_id}'
    driver.get(profile_url)
    time.sleep(5)
    print(f"Processing user: {unique_id} with action: {action}")

    if action == 1:
        load_followings(driver, unique_id)
    elif action == 2 and not check_action_done(unique_id, 'load_videos'):
        load_videos(driver, unique_id)
    elif action == 3:
        print(f"Downloading videos for user: {unique_id}")
        download_top_videos(driver, profile_url, unique_id)
        # Ensure random actions are performed after downloading videos
        perform_random_actions(driver, profile_url)
        save_action_done(unique_id, 'download_videos')
        print(f"Completed downloading videos for user: {unique_id}")

def run_task_in_browser(start_browser_func, unique_ids, action, run_duration, config_file_path):
    driver = start_browser_func()
    if driver:
        end_time = time.time() + run_duration
        try:
            driver.get("https://www.tiktok.com")
            cookies = load_cookies(config_file_path)
            update_browser_cookies(driver, cookies)

            for unique_id in unique_ids:
                if time.time() >= end_time:
                    break
                print(f"Processing user in browser: {unique_id}")
                process_user(driver, unique_id, action)
                save_last_processed_user('last_processed_user.json', unique_id)
                print(f"Finished processing user: {unique_id}")

        except Exception as e:
            print(f"Error during browser operation: {e}")
        finally:
            cookies = driver.get_cookies()
            cookies = validate_cookies(cookies)  # 验证并调整cookie格式
            with open(config_file_path, 'w', encoding='utf-8') as file:
                json.dump(cookies, file)
            driver.quit()
            print("Browser closed.")
    else:
        print("Failed to start the browser")

def kill_processes(process_name):
    try:
        subprocess.run(f'taskkill /F /IM {process_name}.exe', shell=True)
        print(f"Killed all {process_name} processes.")
    except Exception as e:
        print(f"Error killing {process_name} processes: {e}")

def main(action):
    unique_ids = get_user_unique_ids('naoto.hamanaka_followings.json')
    last_processed_user = load_last_processed_user('last_processed_user.json')

    if last_processed_user:
        start_index = unique_ids.index(last_processed_user) + 1
    else:
        start_index = 0

    browsers = [
        ("chrome", start_chrome_browser),
        ("msedge", start_edge_browser),
        ("firefox", start_firefox_browser)
    ]
    browser_index = 0
    run_duration = 5 * 60  # 每个浏览器运行的时间间隔为5分钟
    config_file_path = r"D:\software\tiktok_crawl\config.json"

    while start_index < len(unique_ids):  # 当还有未处理的博主时继续循环
        process_name, browser_func = browsers[browser_index]
        print(f"Starting task with browser: {process_name}")
        run_task_in_browser(browser_func, unique_ids[start_index:], action, run_duration, config_file_path)
        
        # 更新 start_index
        last_processed_user = load_last_processed_user('last_processed_user.json')
        if last_processed_user:
            start_index = unique_ids.index(last_processed_user) + 1
        
        # 切换到下一个浏览器
        browser_index += 1
        if browser_index >= len(browsers):
            browser_index = 0
        
        # 关闭当前浏览器进程
        kill_processes(process_name)
        
        print(f"Switching to next browser: {browsers[browser_index][0]}")

if __name__ == "__main__":
    action = int(input("Please provide an action (1: Load Followings, 2: Load Videos, 3: Download Videos): "))
    main(action)
