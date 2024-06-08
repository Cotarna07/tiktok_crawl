from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import subprocess
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# Firefox安装路径
firefox_path = r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
# 指定GeckoDriver的路径
geckodriver_path = r"C:\Program Files (x86)\Mozilla Firefox\geckodriver.exe"

# 使用subprocess启动Firefox并开启Marionette服务
subprocess.Popen([firefox_path, '-marionette'])

# 等待几秒以确保Firefox启动
time.sleep(5)

# 创建服务，指定Marionette端口为2828，使用--connect-existing参数
firefox_service = Service(executable_path=geckodriver_path, service_args=['--marionette-port', '2828', '--connect-existing'])

# 创建WebDriver实例
driver = webdriver.Firefox(service=firefox_service)

driver.get('https://www.instagram.com/')
time.sleep(20)

driver.quit()  # 关闭浏览器连接