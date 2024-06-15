import time
import random
import os
import mysql.connector
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

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
    video_list_xpath = '//div[@data-e2e="user-post-item-list"]'
    
    try:
        video_list = driver.find_element(By.XPATH, video_list_xpath)
    except Exception as e:
        print(f"Error finding video list: {e}")
        return

    previous_count = 0
    no_new_video_count = 0

    # 将模拟鼠标移动到第二个视频的特定元素处
    second_video_element_xpath = '(//div[@data-e2e="user-post-item-list"]//div[contains(@class, "css-x6y88p-DivItemContainerV2")])[2]'
    try:
        second_video_element = driver.find_element(By.XPATH, second_video_element_xpath)
        actions = ActionChains(driver)
        actions.move_to_element(second_video_element).perform()
    except Exception as e:
        print(f"Error finding or moving to the second video element: {e}")

    while no_new_video_count < 20:
        current_videos = driver.find_elements(By.XPATH, f'{video_list_xpath}//div[contains(@class, "css-x6y88p-DivItemContainerV2")]')
        current_count = len(current_videos)
        print(f"Current count of videos: {current_count}")

        if current_count == previous_count:
            no_new_video_count += 1
            print(f"No new videos loaded, attempt {no_new_video_count}.")
        else:
            no_new_video_count = 0
            previous_count = current_count

        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(random.uniform(1, 3))  # 随机等待时间，模拟人为操作

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
        INSERT INTO `视频信息` (`唯一ID`, `视频链接`, `播放数`, `抓取时间`)
        VALUES (%s, %s, %s, NOW())
        ON DUPLICATE KEY UPDATE `播放数` = VALUES(`播放数`), `抓取时间` = NOW()
    """
    cursor.execute(insert_query, (unique_id, video_data['url'], video_data['play_count']))

if __name__ == "__main__":
    unique_id = 'patriciarodriguez9631'  # 替换为你要测试的博主ID
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    load_videos(driver, unique_id)
    import_video_data_to_database(unique_id)
    
    driver.quit()
