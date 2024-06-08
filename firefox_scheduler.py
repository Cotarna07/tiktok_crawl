import subprocess
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from test_cookie_manager import load_cookies, update_browser_cookies, save_last_processed_user, load_last_processed_user, save_cookies
from random_actions import perform_random_actions
import json
def start_firefox_browser():
    try:
        # 启动Firefox浏览器并开启Marionette服务
        firefox_path = r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
        geckodriver_path = r"C:\Program Files (x86)\Mozilla Firefox\geckodriver.exe"
        subprocess.Popen([firefox_path, '-marionette'])
        time.sleep(5)  # 等待浏览器完全启动

        # 创建服务，指定Marionette端口
        firefox_service = Service(executable_path=geckodriver_path, service_args=['--marionette-port', '2828', '--connect-existing'])

        # 设置Selenium选项以连接到Firefox浏览器
        print("Configuring Selenium options...")
        firefox_options = Options()
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--no-sandbox")

        # 启动WebDriver并连接到已经启动的Firefox浏览器
        print("Connecting to Firefox browser with Selenium...")
        driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
        return driver
    except Exception as e:
        print(f"Error starting Firefox browser: {e}")
        return None

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

    if action == 1:
        perform_random_actions(driver, profile_url)
    # 添加其他动作如load_followers, load_videos, download_top_videos

def main(action):
    last_processed_user_file = 'last_processed_user.json'
    last_processed_user = load_last_processed_user(last_processed_user_file)
    unique_ids = get_user_unique_ids('naoto.hamanaka_followings.json')

    if last_processed_user:
        start_index = unique_ids.index(last_processed_user) + 1
    else:
        start_index = 0

    driver = start_firefox_browser()
    if driver:
        driver.get("https://www.tiktok.com")
        cookies = load_cookies(r"D:\software\tiktok_crawl\config.json")
        update_browser_cookies(driver, cookies)

        for unique_id in unique_ids[start_index:]:
            process_user(driver, unique_id, action)
            save_last_processed_user(last_processed_user_file, unique_id)
        
        save_cookies(driver, r"D:\software\tiktok_crawl\config.json")
        driver.quit()

if __name__ == "__main__":
    action = int(input("Please provide an action number (1, 2, or 3): "))
    main(action)
