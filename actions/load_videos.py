import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import os
import mysql.connector

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

def scroll_and_load_all_videos(driver):
    print("Scrolling to load all videos...")
    video_list_xpath = '/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[3]/div'
    
    try:
        # 等待视频列表容器加载完成
        video_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, video_list_xpath)))
    except Exception as e:
        print(f"Error finding video list: {e}")
        return

    previous_count = 0
    no_new_video_count = 0

    while no_new_video_count < 20:
        current_videos = driver.find_elements(By.XPATH, f'{video_list_xpath}/div')
        current_count = len(current_videos)
        print(f"Current count of videos: {current_count}")

        if current_count == previous_count:
            no_new_video_count += 1
            print(f"No new videos loaded, attempt {no_new_video_count}.")
        else:
            no_new_video_count = 0
            previous_count = current_count

        scroll_height = random.randint(500, 800)  # 随机翻滚距离
        driver.execute_script(f"arguments[0].scrollTop += {scroll_height};", video_list)
        time.sleep(0.1)  # 短时间等待

    print("Stopping scroll as no new videos loaded for twenty consecutive attempts.")

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
                
                # 处理带有小数点的情况
                if 'K' in play_count_str:
                    play_count = float(play_count_str.replace('K', '')) * 1000
                elif 'M' in play_count_str:
                    play_count = float(play_count_str.replace('M', '')) * 1000000
                else:
                    play_count = float(play_count_str.replace(',', ''))
                
                video_data.append({'url': video_url, 'play_count': int(play_count)})
        except Exception as e:
            print(f"Error extracting video data: {e}")
    return video_data

def save_video_data_to_file(unique_id, video_data):
    output_folder = os.path.join(os.getcwd(), '视频数据')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_file_path = os.path.join(output_folder, f'{unique_id}.txt')
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for video in video_data:
            file.write(f"{video['url']},{video['play_count']}\n")

def load_videos(driver, unique_id):
    profile_url = f'https://www.tiktok.com/@{unique_id}'
    driver.get(profile_url)
    time.sleep(5)
    scroll_and_load_all_videos(driver)
    video_data = extract_video_data(driver)
    save_video_data_to_file(unique_id, video_data)
    print(f"Extracted video data for {unique_id}: {video_data}")

def import_video_data_to_database(unique_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    
    output_folder = os.path.join(os.getcwd(), '视频数据')
    output_file_path = os.path.join(output_folder, f'{unique_id}.txt')

    with open(output_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            video_url, play_count = line.strip().split(',')
            video_data = {'url': video_url, 'play_count': int(play_count)}
            save_video_data(cursor, unique_id, video_data)
    
    connection.commit()
    cursor.close()
    connection.close()

# 示例的保存到数据库的函数
def save_video_data(cursor, unique_id, video_data):
    insert_query = """
        INSERT INTO `视频` (`用户ID`, `视频链接`, `播放次数`, `抓取时间`)
        VALUES (%s, %s, %s, NOW())
        ON DUPLICATE KEY UPDATE `播放次数` = VALUES(`播放次数`), `抓取时间` = NOW()
    """
    cursor.execute(insert_query, (unique_id, video_data['url'], video_data['play_count']))

if __name__ == "__main__":
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    unique_id = 'patriciarodriguez9631'  # 替换为你要测试的博主ID
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    load_videos(driver, unique_id)
    import_video_data_to_database(unique_id)
    
    driver.quit()
