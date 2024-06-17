import json
import time
import subprocess
import pandas as pd
from utils.cookie_manager import load_cookies, update_browser_cookies, save_last_processed_user, load_last_processed_user, save_cookies, validate_cookies
from utils.browser_scheduler import start_chrome_browser, start_edge_browser, start_firefox_browser, kill_processes
from actions.download_videos import download_top_videos
from utils.random_actions import perform_random_actions
from actions.load_followers import load_list, import_list_to_database
from actions.load_videos import load_videos

# 读取Excel文件
def read_excel(file_path):
    print(f"Reading Excel file: {file_path}")
    df = pd.read_excel(file_path)
    print("Excel file read successfully")
    return df

# 更新Excel文件
def update_excel(file_path, df):
    print(f"Updating Excel file: {file_path}")
    df.to_excel(file_path, index=False)
    print("Excel file updated successfully")

# 处理用户任务
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
        download_top_videos(driver, profile_url, unique_id)
        perform_random_actions(driver, profile_url)
        print(f"Completed downloading videos for user: {unique_id}")

# 运行浏览器任务
def run_task_in_browser(start_browser_func, df, run_duration, config_file_path):
    driver = start_browser_func()
    if driver:
        end_time = time.time() + run_duration
        try:
            driver.get("https://www.tiktok.com")
            cookies = load_cookies(config_file_path)
            update_browser_cookies(driver, cookies)

            # 处理动作一的任务
            for action_num, sub_action, user_column, status_column in [(1, '关注列表', '动作一关注列表_用户ID', '动作一_关注列表_执行'),
                                                                      (1, '粉丝列表', '动作一_粉丝列表_用户ID', '动作一_粉丝列表_执行')]:
                user_to_process = df[(df[user_column].notna()) & (df[status_column].fillna(0) == 0)].iloc[0]
                process_user(driver, user_to_process[user_column], action_num, sub_action)
                df.at[user_to_process.name, status_column] = 1

            # 动态交替执行动作二和动作三
            while time.time() < end_time:
                for action_num, user_column, status_column in [(2, '动作二_用户ID', '动作二_执行'), 
                                                               (3, '动作三_用户ID', '动作三_执行')]:
                    available_users = df[(df[user_column].notna()) & (df[status_column].fillna(0) == 0)]
                    if not available_users.empty:
                        user_to_process = available_users.iloc[0]
                        process_user(driver, user_to_process[user_column], action_num)
                        df.at[user_to_process.name, status_column] = 1
                    if time.time() >= end_time:
                        break

            cookies = driver.get_cookies()
            cookies = validate_cookies(cookies)
            with open(config_file_path, 'w', encoding='utf-8') as file:
                json.dump(cookies, file)

        except Exception as e:
            print(f"Error during browser operation: {e}")
        finally:
            driver.quit()
            print("Browser closed.")
    else:
        print("Failed to start the browser")

# 主函数
def main(excel_file):
    print(f"Starting main function with Excel file: {excel_file}")
    df = read_excel(excel_file)
    print("Initial DataFrame:\n", df.head())
    browsers = [
        ("chrome", start_chrome_browser),
        ("msedge", start_edge_browser),
        ("firefox", start_firefox_browser)
    ]
    browser_index = 0
    run_duration = 30 * 60
    config_file_path = r"D:\software\tiktok_crawl\config.json"

    while True:
        process_name, browser_func = browsers[browser_index]
        print(f"Starting task with browser: {process_name}")
        run_task_in_browser(browser_func, df, run_duration, config_file_path)

        browser_index = (browser_index + 1) % len(browsers)
        kill_processes(process_name)
        print(f"Switching to next browser: {browsers[browser_index][0]}")

        update_excel(excel_file, df)

if __name__ == "__main__":
    main(r"D:\software\tiktok_crawl\任务表格.xlsx")
