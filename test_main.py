import json
import time
import subprocess
from test_cookie_manager import load_cookies, update_browser_cookies, save_last_processed_user, load_last_processed_user, save_cookies, validate_cookies
from random_actions import perform_random_actions
from test_browser_scheduler import start_chrome_browser, start_edge_browser, start_firefox_browser
from actions.download_videos import download_top_videos
from database_manager import check_action_done, save_action_done
from actions import load_videos

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
    elif action == 2 and not check_action_done(unique_id, 'load_videos'):
        load_videos(driver, unique_id)
    elif action == 3:
        download_top_videos(driver, profile_url, unique_id)
        perform_random_actions(driver, profile_url)
        save_action_done(unique_id, 'download_videos')

def run_task_in_browser(start_browser_func, unique_ids, action, run_duration, config_file_path):
    driver = start_browser_func()
    if driver:
        end_time = time.time() + run_duration
        try:
            driver.get("https://www.tiktok.com")
            cookies = load_cookies(config_file_path)
            update_browser_cookies(driver, cookies)

            while time.time() < end_time:
                for unique_id in unique_ids:
                    process_user(driver, unique_id, action)
                    save_last_processed_user('last_processed_user.json', unique_id)
                    if time.time() >= end_time:
                        break
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

    while True:
        process_name, browser_func = browsers[browser_index]
        print(f"Starting task with browser: {process_name}")
        run_task_in_browser(browser_func, unique_ids[start_index:], action, run_duration, config_file_path)
        
        # 切换到下一个浏览器
        browser_index += 1
        if browser_index >= len(browsers):
            browser_index = 0
        
        # 关闭当前浏览器进程
        kill_processes(process_name)
        
        print(f"Switching to next browser: {browsers[browser_index][0]}")

if __name__ == "__main__":
    action = int(input("Please provide an action number (1, 2, or 3): "))
    main(action)
