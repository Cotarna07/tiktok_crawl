import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from database_manager import save_video_data, check_action_done, save_action_done

def scroll_and_load_all_videos(driver):
    print("Scrolling to load all videos...")
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)  # 等待页面加载更多视频
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

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

def load_videos(driver, unique_id):
    profile_url = f'https://www.tiktok.com/@{unique_id}'

    if not check_action_done(unique_id, 'load_videos'):
        driver.get(profile_url)
        time.sleep(5)
        scroll_and_load_all_videos(driver)
        video_data = extract_video_data(driver)
        save_video_data(unique_id, video_data)
        save_action_done(unique_id, 'load_videos')
        print(f"Extracted video data for {unique_id}: {video_data}")
