import os
import subprocess
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from test_cookie_manager import load_cookies, update_browser_cookies, save_last_processed_user, load_last_processed_user, save_cookies
from actions.load_followers import load_followers
from actions.load_videos import load_videos
from actions.download_videos import download_top_videos
from database_manager import check_action_done, save_action_done

def start_browser():
    print("Starting browser...")
    subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--remote-debugging-port=9222"])
    time.sleep(5)

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

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
    if action == 1 and not check_action_done(unique_id, 'load_followers'):
        load_followers(driver, unique_id)
    elif action == 2 and not check_action_done(unique_id, 'load_videos'):
        load_videos(driver, unique_id)
    elif action == 3:
        download_top_videos(driver, profile_url, unique_id)

def main(action):
    last_processed_user_file = 'last_processed_user.json'
    last_processed_user = load_last_processed_user(last_processed_user_file)
    unique_ids = get_user_unique_ids('naoto.hamanaka_followings.json')

    if last_processed_user:
        start_index = unique_ids.index(last_processed_user) + 1
    else:
        start_index = 0

    driver = start_browser()
    driver.get("https://www.tiktok.com")
    cookies = load_cookies(r"D:\software\tiktok_crawl\config.json")  # 确保这里提供了正确的路径
    update_browser_cookies(driver, cookies)

    for unique_id in unique_ids[start_index:]:
        process_user(driver, unique_id, action)
        save_last_processed_user(last_processed_user_file, unique_id)

    # 保存更新后的cookies
    save_cookies(driver, r"D:\software\tiktok_crawl\config.json")
    driver.quit()

if __name__ == "__main__":
    action = int(input("Please provide an action number (1, 2, or 3): "))
    main(action)
