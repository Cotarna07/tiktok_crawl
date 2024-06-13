from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

def scroll_followers_list(driver):
    try:
        followers_list_xpath = '//div[contains(@class, "DivUserListContainer")]'
        followers_list = driver.find_element(By.XPATH, followers_list_xpath)
        
        initial_accounts = driver.find_elements(By.XPATH, f'{followers_list_xpath}//a[@class="es616eb3 css-5c23qb-StyledLink-StyledUserInfoLink er1vbsz0"]')
        initial_count = len(initial_accounts)
        print(f"Initial count of accounts: {initial_count}")
        
        no_new_account_count = 0  # 用于记录连续三次没有加载出新账号的次数
        
        while no_new_account_count < 3:
            follow_button = driver.find_element(By.XPATH, '/html/body/div[8]/div/div[2]/div/div/div[2]/div/div/section/div/div[3]/li[1]/div/div/div/div/button')
            actions = ActionChains(driver)
            actions.move_to_element(follow_button).perform()
            
            # 随机滚动步长范围：current_count的100倍至200倍
            scroll_height = random.randint(initial_count * 100, initial_count * 200)
            driver.execute_script(f"arguments[0].scrollTop += {scroll_height};", followers_list)
            time.sleep(2)  # 等待加载新内容
            
            current_accounts = driver.find_elements(By.XPATH, f'{followers_list_xpath}//a[@class="es616eb3 css-5c23qb-StyledLink-StyledUserInfoLink er1vbsz0"]')
            current_count = len(current_accounts)
            print(f"Current count of accounts: {current_count}")
            
            if current_count == initial_count:
                no_new_account_count += 1
                print(f"No new accounts loaded, attempt {no_new_account_count}.")
            else:
                no_new_account_count = 0  # 如果加载出了新账号，重置计数器
                initial_count = current_count
        
        print("Stopping scroll as no new accounts loaded for three consecutive attempts.")
    except Exception as e:
        print(f"Error scrolling followers list: {e}")

def load_followers(driver, unique_id):
    profile_url = f'https://www.tiktok.com/@{unique_id}'
    driver.get(profile_url)
    time.sleep(5)  # 等待页面加载
    try:
        followers_button = driver.find_element(By.XPATH, '//strong[@title="粉丝"]')
        followers_button.click()
        time.sleep(5)  # 等待粉丝页面加载
        scroll_followers_list(driver)
    except Exception as e:
        print(f"Error clicking followers button or scrolling: {e}")

def load_following(driver, unique_id):
    profile_url = f'https://www.tiktok.com/@{unique_id}'
    driver.get(profile_url)
    time.sleep(5)  # 等待页面加载
    try:
        following_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div[1]/h3/div[1]/span')
        following_button.click()
        time.sleep(5)  # 等待关注页面加载
        scroll_followers_list(driver)  # 使用相同的滚动逻辑
    except Exception as e:
        print(f"Error clicking following button or scrolling: {e}")

if __name__ == "__main__":
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    unique_id = 'patriciarodriguez9631'  # 替换为你要测试的博主ID
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    action = input("Please provide an action (load_followers, load_following): ")

    if action == "load_followers":
        load_followers(driver, unique_id)
    elif action == "load_following":
        load_following(driver, unique_id)
    
    driver.quit()
