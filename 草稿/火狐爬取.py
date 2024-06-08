import subprocess
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re
import instaloader
import random
import datetime
import os
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Firefox安装路径
firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
# 指定GeckoDriver的路径
geckodriver_path = r"C:\Program Files\Mozilla Firefox\geckodriver.exe"

# 使用subprocess启动Firefox并开启Marionette服务
subprocess.Popen([firefox_path, '-marionette'])

# 等待几秒以确保Firefox启动
time.sleep(5)

# 创建服务，指定Marionette端口为2828，使用--connect-existing参数
firefox_service = Service(executable_path=geckodriver_path, service_args=['--marionette-port', '2828', '--connect-existing'])

# 创建WebDriver实例
driver = webdriver.Firefox(service=firefox_service)

# 创建 Instaloader 实例
L = instaloader.Instaloader()

# 打开一个具体的 Instagram 页面（替换成实际的用户主页 URL）
driver.get('https://www.instagram.com/')
time.sleep(15)

# 假设的配置文件路径和Selenium WebDriver实例
config_file_path = r"D:\BaiduNetdiskDownload\广告素材\历史广告\大码\爬虫代码\数据处理\爬虫\firefox爬虫\firefox_cookie.json"

# 载入配置文件
with open('config.json', 'r') as f:
    config = json.load(f)

def update_instaloader_session_with_browser_cookies(driver, instaloader_instance):
    """
    使用浏览器中的cookie更新Instaloader的会话。
    """
    browser_cookies = driver.get_cookies()
    session_cookies = {}
    for cookie in browser_cookies:
        session_cookies[cookie['name']] = cookie['value']
    instaloader_instance.context._session.cookies.clear()
    instaloader_instance.context._session.cookies.update(session_cookies)

def load_config(config_file_path):
    """载入配置文件"""
    with open(config_file_path, 'r') as file:
        return json.load(file)

# 更新配置文件
def update_config(config, config_file_path):
    with open(config_file_path, 'w') as f:
        json.dump(config, f, indent=4)

# 找到页面上的账户名
def find_account_name(driver):
    xpath = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[8]/div/span/div/a'
    element = driver.find_element(By.XPATH, xpath)
    account_url = element.get_attribute('href')
    account_name = account_url.split('/')[-2]
    return account_name

# 从浏览器获取当前的 cookies，并更新配置文件
def update_config_with_browser_cookies(driver, account_name, config):
    updated_cookies = driver.get_cookies()
    for account in config['accounts']:
        if account['username'] == account_name:
            account['cookies'] = updated_cookies
            print(f"Cookies for account {account_name} have been updated in the config.")
            break
    save_config(config_file_path, config)

# 函数来保存配置文件
def save_config(path, config):
    with open(path, 'w') as file:
        json.dump(config, file, indent=4)

def update_browser_cookies(driver, cookies):
    driver.delete_all_cookies()
    for cookie in cookies:
        # 调整 'expiry' 字段
        if 'expiry' in cookie:
            cookie['expiry'] = cookie.pop('expirationDate')
        # 调整 'sameSite' 字段
        if 'sameSite' in cookie:
            if cookie['sameSite'] not in ["Strict", "Lax", "None"]:
                # 如果 'sameSite' 值不合法，可以选择删除该属性或设置为默认值
                del cookie['sameSite']  # 或 cookie['sameSite'] = "Lax" 作为示例
        driver.add_cookie(cookie)
        
def main(driver, config_file_path):
    config = load_config(config_file_path)
    current_account_index = config.get('current_account_index', 0)
    accounts = config['accounts']
    current_account = accounts[current_account_index]
    
    # 更新浏览器中的cookie
    update_browser_cookies(driver, current_account['cookies'])
    print(f"Updated cookies for {current_account['username']} in the browser.")
    
    # 更新当前账户索引以及配置文件
    config['current_account_index'] = (current_account_index + 1) % len(accounts)
    save_config(config_file_path, config)  # 此处应传递 config_file_path 作为第一个参数

def is_reel_content_in_file(file_path, reel_content):
    if not os.path.exists(file_path):
        return False
    with open(file_path, 'r') as file:
        existing_contents = set(line.strip() for line in file)
    return reel_content in existing_contents

def switch_cookie_and_update_instaloader(driver, instaloader_instance, config_file_path):
    """
    切换到下一个账户的 cookies，并更新 Instaloader 的会话。

    :param driver: 浏览器驱动实例。
    :param instaloader_instance: Instaloader 实例。
    :param config_file_path: 配置文件路径。
    """
    # 载入配置文件
    config = load_config(config_file_path)
    
    # 计算下一个账户的索引
    current_account_index = config.get('current_account_index', 0)
    next_account_index = (current_account_index + 1) % len(config['accounts'])
    next_account = config['accounts'][next_account_index]
    
    # 更新浏览器中的 cookies
    update_browser_cookies(driver, next_account['cookies'])
    
    # 更新 Instaloader 的会话 cookies
    update_instaloader_session_with_browser_cookies(driver, instaloader_instance)
    
    # 更新配置文件以反映新的当前账户索引
    config['current_account_index'] = next_account_index
    save_config(config_file_path, config)
    
    print(f"Switched to account: {next_account['username']}")

# 更新浏览器cookies并同步至Instaloader
def switch_cookie_and_update_instaloader(driver, instaloader_instance, config_file_path):
    config = load_config(config_file_path)
    current_account_index = config.get('current_account_index', 0)
    next_account_index = (current_account_index + 1) % len(config['accounts'])
    next_account = config['accounts'][next_account_index]

    driver.delete_all_cookies()
    for cookie in next_account['cookies']:
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry'])
        # 确保 'sameSite' 属性存在且值有效
        if 'sameSite' not in cookie or cookie['sameSite'] not in ["Strict", "Lax", "None"]:
            cookie['sameSite'] = "Lax"  # 设置默认值为 "Lax"
        driver.add_cookie(cookie)
    
    # 更新 Instaloader 的会话 cookies
    update_instaloader_session_with_browser_cookies(driver, instaloader_instance)
    
    # 更新配置文件以反映新的当前账户索引
    config['current_account_index'] = next_account_index
    save_config(config_file_path, config)
    
    print(f"Switched to account: {next_account['username']}")

    # 更新配置文件中的当前账户索引
    config['current_account_index'] = next_account_index
    with open(config_file_path, 'w') as file:
        json.dump(config, file, indent=4)


reel_contents_file = 'reel_contents.txt'
success_log_file = 'success_log.txt'
error_log_file = 'error_log.txt'
# 定义失败日志文件名
failed_log_file = 'failed_log_file.txt'

reel_contents_set = set()

failed_count = 0
error_count = 0  # 新增变量用于跟踪连续错误次数

#最大下载数量
max_reels_per_link = 2

# 初始切换cookies
switch_cookie_and_update_instaloader(driver, L, config_file_path)

# 初始化上次检查时间
last_cookie_switch_time = time.time()
# 设置更换cookie的间隔，例如600到660秒
cookie_switch_interval = random.randint(60, 70)

try:  
    while True:  # 无限循环直到用户中断  

        try:  
            # 读取 links.txt 到列表  
            with open('links.txt', 'r') as file:  
                links = [link.strip() for link in file]  
        
            # 读取 success_log.txt 文件中倒数第一行的链接  
            with open(success_log_file, 'r') as success_file:  
                lines = success_file.readlines()  
                if len(lines) >= 1:  
                    prev_link = lines[-1].strip()  
                    if prev_link in links:  
                        start_index = links.index(prev_link) + 1  
                        # 如果已经是最后一个链接，则从头开始  
                        if start_index >= len(links):  
                            start_index = 0  
                            
                            # 清空文件
                            with open(success_log_file, 'w') as success_clear:
                                pass  
                    else:  
                        start_index = 0  
                else:  
                    start_index = 0  
                    
            for i in range(start_index, len(links)):  
                link = links[i] 

                current_time = time.time()  # 更新当前时间
                if current_time - last_cookie_switch_time > cookie_switch_interval:
                    switch_cookie_and_update_instaloader(driver, L, config_file_path)
                    last_cookie_switch_time = current_time  # 更新上次检查时间
                    cookie_switch_interval = random.randint(600, 660)  # 可选：重新设置间隔
                    print("Cookies have been switched.")

                with open(success_log_file, 'a') as success_log:
                    success_log.write(f"{link}\n") 
                try:  
                    driver.get(link)  
        
                    # 生成一个10到20之间的随机秒数（包括10和20）  
                    sleep_time = random.uniform(20, 30)  
        
                    # 等待随机生成的时间  
                    time.sleep(sleep_time)  
        
                    wait = WebDriverWait(driver, 20)  # Adjust this timeout as needed  
        
                    reel_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/reel/")]')))  
        
                    reel_count = 0  # 添加一个计数器来跟踪已下载的reel_content数量  
        
                    for reel_link in reel_links:  
                        href = reel_link.get_attribute('href')  

                        match = re.search(r'/reel/(.*)/', href)  
                        if match:  # Check if a match was found before trying to access .group(1)  
                            reel_content = match.group(1)  
                            # 检查短链接是否已存在于文件中，如果不存在则写入文件  
                            if not is_reel_content_in_file(reel_contents_file, reel_content):  
                                with open(reel_contents_file, 'a') as file:  
                                    file.write(f"{reel_content}\n")  
                                print(reel_content)  
                                reel_contents_set.add(reel_content)  
        
                                # 仅在未达到最大下载量时才尝试下载  
                                if reel_count < max_reels_per_link:  
                                    try:  
                                        post = instaloader.Post.from_shortcode(L.context, reel_content)  
                                        os.makedirs(reel_content, exist_ok=True)  
                                        L.download_post(post, target=f'{reel_content}')  
                                        print(f"Downloaded Reel with shortcode: {reel_content}")  
        
                                        # 在视频文件夹内创建一个文本文件，并写入链接  
                                        with open(os.path.join(reel_content, f'{reel_content}_link.txt'), 'w') as link_file:  
                                            link_file.write(link)  
        
                                        reel_count += 1  
        
                                    except Exception as e:  
                                        print(f"Failed to download Reel with shortcode: {reel_content}. Error: {e}")
                                            # 将下载失败的 reel_content 记录到失败日志文件中
                                        with open(failed_log_file, 'a') as file:
                                            file.write(f"{link}\n{reel_content}\n")  
        
                                # 如果已经达到最大下载量，则跳出循环  
                                if reel_count >= max_reels_per_link:  
                                    break  
        
                except Exception as e:
                    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                    error_message = f"Error processing link {link} at {current_time}: {e}\n"
                    with open(error_log_file, 'a') as log_file:
                        log_file.write(error_message)
                    print(error_message.strip())

            if start_index > 0 and start_index < len(links):  # 如果不是从头开始且未达到末尾  
                continue  # 继续下一次循环，避免重新从start_index开始遍历  
  
            # 如果已经遍历到末尾或者从头开始，则重置start_index并继续循环  
            start_index = 0 
             
        except KeyboardInterrupt:  
            print("程序被用户中断，正在退出...")  
            break  # 当用户按下Ctrl+C时退出循环 
  
finally:  
    driver.quit()  # 关闭浏览器连接