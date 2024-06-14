import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import random

def start_chrome_browser():
    subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--remote-debugging-port=9222"])
    time.sleep(5)
    
    options = ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=options)
    return driver

def scroll_and_load_all_videos(driver):
    print("Scrolling to load all videos...")
    driver.get("https://www.youtube.com/")
    time.sleep(5)  # 等待页面加载
    
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(random.uniform(1, 3))  # 随机等待时间，模拟人为操作
        print("Scrolling...")

if __name__ == "__main__":
    driver = start_chrome_browser()
    scroll_and_load_all_videos(driver)
    driver.quit()
