import os
import time
from selenium.webdriver.common.by import By
from yt_dlp import YoutubeDL

def download_video(video_url, save_path):
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
        try:
            ydl.download([video_url])
        except Exception as e:
            print(f"Error downloading video {video_url}: {e}")

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
        print(f"Downloading video {i+1} for user: {unique_id}")
        save_path = os.path.join(save_dir, f"video_{i+1}.mp4")
        download_video(video['url'], save_path)
    print(f"Downloaded {len(video_data[:max_videos])} videos for user: {unique_id}")
