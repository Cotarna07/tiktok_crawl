import time
import subprocess
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def start_browser():
    print("Starting browser...")
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    subprocess.Popen([chrome_path, "--remote-debugging-port=9222"])
    time.sleep(5)

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def test_click_video(driver, profile_url):
    print(f"Visiting profile: {profile_url}")
    driver.get(profile_url)
    time.sleep(20)  # 增加等待时间，确保页面加载

    # 视频的XPath列表
    video_xpaths = [
        '/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div/a',
        '/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[2]/div/div[1]/div[1]/div/div/a',
        '/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[2]/div/div[3]/div[1]/div/div/a',
        '/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[2]/div/div[5]/div[1]/div/div/a',
        '/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[2]/div/div[4]/div[1]/div/div/a'
    ]

    # 随机选择一个XPath并点击
    try:
        random_xpath = random.choice(video_xpaths)
        video_element = driver.find_element(By.XPATH, random_xpath)
        print("Video element found.")
        video_element.click()  # 点击视频
        print("Clicked on video.")
        time.sleep(random.randint(4, 6))  # 播放4到6秒

        # 随机点赞，10%的概率
        if random.random() < 0.1:
            try:
                like_button_xpath = '/html/body/div[1]/div[2]/div[4]/div/div[2]/div[1]/div/div[1]/div[2]/div/div[1]/div[1]/button[1]'
                like_button = driver.find_element(By.XPATH, like_button_xpath)
                like_button.click()
                print("Liked the video.")
            except Exception as e:
                print(f"Error finding or clicking like button: {e}")

        driver.back()  # 返回上一页
        print("Returned to profile page.")
    except Exception as e:
        print(f"Error finding or clicking video element: {e}")

def main():
    profile_url = 'https://www.tiktok.com/@faithhelizabethhh'  # 替换为实际的博主主页URL
    driver = start_browser()
    test_click_video(driver, profile_url)
    driver.quit()

if __name__ == "__main__":
    main()
