import json
import time
import subprocess
from utils.cookie_manager import load_cookies, update_browser_cookies, save_last_processed_user, load_last_processed_user, save_cookies, validate_cookies
from utils.browser_scheduler import start_chrome_browser, start_edge_browser, start_firefox_browser, kill_processes
from actions.download_videos import download_top_videos
from utils.random_actions import perform_random_actions
from actions.load_followers import load_list, import_list_to_database  # Ensure these functions are correctly defined and imported
from actions.load_videos import load_videos

def get_user_unique_ids(json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return [user['user']['uniqueId'] for user in data]
    except Exception as e:
        print(f"Error loading user unique IDs: {e}")
        return []

def process_user(driver, unique_id, action, sub_action=None):
    profile_url = f'https://www.tiktok.com/@{unique_id}'
    driver.get(profile_url)
    time.sleep(5)
    print(f"Processing user: {unique_id} with action: {action}")

    if action == 1:
        if sub_action == '粉丝列表':
            load_list(driver, unique_id, '粉丝列表')
        elif sub_action == '关注列表':
            load_list(driver, unique_id, '关注列表')
        import_list_to_database(unique_id, sub_action)
    elif action == 2:
        load_videos(driver, unique_id)
    elif action == 3:
        print(f"Downloading videos for user: {unique_id}")
        download_top_videos(driver, profile_url, unique_id)
        perform_random_actions(driver, profile_url)
        print(f"Completed downloading videos for user: {unique_id}")

def run_task_in_browser(start_browser_func, unique_ids, action, sub_action, run_duration, config_file_path):
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
                process_user(driver, unique_id, action, sub_action)
                save_last_processed_user('last_processed_user.json', unique_id)
                print(f"Finished processing user: {unique_id}")

        except Exception as e:
            print(f"Error during browser operation: {e}")
        finally:
            cookies = driver.get_cookies()
            cookies = validate_cookies(cookies)
            with open(config_file_path, 'w', encoding='utf-8') as file:
                json.dump(cookies, file)
            driver.quit()
            print("Browser closed.")
    else:
        print("Failed to start the browser")

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
    run_duration = 5 * 60
    config_file_path = r"D:\software\tiktok_crawl\config.json"

    if action == 1:
        sub_action = input("Please provide a sub-action (粉丝列表, 关注列表): ")
    else:
        sub_action = None

    while start_index < len(unique_ids):
        process_name, browser_func = browsers[browser_index]
        print(f"Starting task with browser: {process_name}")
        run_task_in_browser(browser_func, unique_ids[start_index:], action, sub_action, run_duration, config_file_path)
        
        last_processed_user = load_last_processed_user('last_processed_user.json')
        if last_processed_user:
            start_index = unique_ids.index(last_processed_user) + 1
        
        browser_index += 1
        if browser_index >= len(browsers):
            browser_index = 0
        
        kill_processes(process_name)
        
        print(f"Switching to next browser: {browsers[browser_index][0]}")

if __name__ == "__main__":
    action = int(input("Please provide an action number (1, 2, or 3): "))
    main(action)
