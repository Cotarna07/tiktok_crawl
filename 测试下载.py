import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def start_browser():
    print("Starting browser...")
    subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--remote-debugging-port=9222"])
    time.sleep(5)

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def test_browser_control():
    driver = start_browser()
    driver.get('https://www.tiktok.com')
    time.sleep(5)  # 等待几秒钟以确保页面加载完成
    print("Page title:", driver.title)
    driver.quit()

if __name__ == "__main__":
    test_browser_control()
