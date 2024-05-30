import os
import subprocess
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from yt_dlp import YoutubeDL
from test_cookie_manager import load_cookies, update_browser_cookies, save_last_processed_user, load_last_processed_user
from random_actions import perform_random_actions

def start_browser():
    print("Starting browser...")
    subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--remote-debugging-port=9222"])
    time.sleep(5)

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def download_video(video_url, save_path):
    try:
        ydl_opts = {
            'outtmpl': save_path,
            'format': 'bestvideo+bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except Exception as e:
        print(f"yt-dlp failed, falling back to HTTP download: {e}")
        response = requests.get(video_url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Downloaded {save_path} via HTTP")
        else:
            print(f"Failed to download {video_url} via HTTP")

def extract_video_data(driver):
    video_data = []
    print("Extracting video data...")
    time.sleep(5)  # 增加等待时间，确保页面完全加载

    video_elements = driver.find_elements(By.XPATH, '//div[@class="css-x6y88p-DivItemContainerV2 e19c29qe8"]')
    if not video_elements:
        print("No video elements found with the provided XPath.")
    
    for video in video_elements:
        try:
            video_url = video.find_element(By.XPATH, './/a').get_attribute('href')
            if "/video/" in video_url:
                play_count_element = video.find_element(By.XPATH, './/strong[@data-e2e="video-views"]')
                play_count_str = play_count_element.text if play_count_element else '0'
                play_count = int(play_count_str.replace('K', '000').replace('M', '000000'))
                video_data.append({'url': video_url, 'play_count': play_count})
        except Exception as e:
            print(f"Error extracting video data: {e}")
    return video_data

def download_top_videos(driver, profile_url, unique_id, max_videos=2):
    print(f"Visiting profile: {profile_url}")
    driver.get(profile_url)
    time.sleep(10)  # 增加等待时间，确保页面完全加载

    video_data = extract_video_data(driver)
    if not video_data:
        print("No video data found.")
        return

    save_dir = os.path.join(r"D:\software\tiktok_crawl\download", unique_id)
    os.makedirs(save_dir, exist_ok=True)

    video_data.sort(key=lambda x: x['play_count'], reverse=True)
    for i, video in enumerate(video_data[:max_videos]):
        save_path = os.path.join(save_dir, f"video_{i+1}.mp4")
        download_video(video['url'], save_path)
        
def process_user(driver, unique_id):
    profile_url = f'https://www.tiktok.com/@{unique_id}'
    download_top_videos(driver, profile_url, unique_id)
    perform_random_actions(driver, profile_url)

def get_user_unique_ids(json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return [user['user']['uniqueId'] for user in data]
    except Exception as e:
        print(f"Error loading user unique IDs: {e}")
        return []

def main(action):
    config_file_path = r"D:\software\tiktok_crawl\config.json"
    json_file_path = r"D:\software\tiktok_crawl\naoto.hamanaka_followings.json"
    last_processed_user_file = r"D:\software\tiktok_crawl\last_processed_user.json"

    cookies = load_cookies(config_file_path)
    user_unique_ids = get_user_unique_ids(json_file_path)

    last_processed_user = load_last_processed_user(last_processed_user_file)
    if last_processed_user:
        start_index = user_unique_ids.index(last_processed_user) + 1
    else:
        start_index = 0

    driver = start_browser()
    driver.get('https://www.tiktok.com')
    time.sleep(3)
    update_browser_cookies(driver, cookies)
    driver.refresh()

    if action == '3':
        for unique_id in user_unique_ids[start_index:]:
            process_user(driver, unique_id)
            save_last_processed_user(last_processed_user_file, unique_id)
    
    driver.quit()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        action = sys.argv[1]
        print(f"Action selected: {action}")
        main(action)
    else:
        print("Please provide an action number (1, 2, or 3).")
