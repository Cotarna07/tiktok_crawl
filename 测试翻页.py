import json
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui

import pyautogui
import time

def start_chrome_browser():
    subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--remote-debugging-port=9222"])
    time.sleep(5)

    options = ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=options)
    return driver

def scroll_page(driver):
    try:
        # 定位到你想悬停的位置
        element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div[1]/h2')
        actions = webdriver.ActionChains(driver)
        actions.move_to_element(element).perform()
        time.sleep(2)

        # 获取元素的位置
        location = element.location
        size = element.size
        x = location['x'] + size['width'] // 2
        y = location['y'] + size['height'] // 2

        # 模拟鼠标中键点击并向下移动100个单位
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown(button='middle')
        time.sleep(1)
        pyautogui.moveTo(x, y + 100)
        # pyautogui.mouseUp(button='middle')
        time.sleep(2)

        print("Mouse middle click and move action performed.")

    except Exception as e:
        print(f"Error during scrolling test: {e}")

if __name__ == "__main__":
    driver = start_chrome_browser()
    driver.get("https://www.tiktok.com/@naoto.hamanaka")
    time.sleep(5)
    
    scroll_page(driver)
    
    driver.quit()
