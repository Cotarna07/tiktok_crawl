import time
from selenium.webdriver.common.by import By
from database_manager import save_follower_data, check_action_done, save_action_done

def get_follower_count(driver):
    try:
        followers = driver.find_element(By.XPATH, '//span[contains(@class, "followers")]').text
        return int(followers.replace('K', '000').replace('M', '000000'))
    except Exception as e:
        print(f"Error getting follower count: {e}")
        return 0

def get_followers(driver, profile_url):
    print(f"Visiting followers page: {profile_url}/followers")
    driver.get(profile_url + '/followers')
    time.sleep(5)  # 等待页面加载

    followers_data = []
    while True:
        follower_elements = driver.find_elements(By.XPATH, '//div[@class="follower-element-class"]')  # 替换为实际的粉丝元素XPath
        if not follower_elements:
            print("No more followers found.")
            break

        for follower in follower_elements:
            try:
                follower_url = follower.find_element(By.XPATH, './/a').get_attribute('href')
                followers_data.append(follower_url)
            except Exception as e:
                print(f"Error extracting follower data: {e}")

        try:
            next_button = driver.find_element(By.XPATH, '//button[contains(text(), "Load more")]')  # 替换为实际的“加载更多”按钮XPath
            next_button.click()
            time.sleep(2)
        except Exception:
            print("No more followers to load.")
            break

    return followers_data

def load_followers(driver, unique_id):
    profile_url = f'https://www.tiktok.com/@{unique_id}'

    if not check_action_done(unique_id, 'load_followers'):
        follower_count = get_follower_count(driver)
        if 6000 <= follower_count <= 100000:
            followers_data = get_followers(driver, profile_url)
            save_follower_data(unique_id, followers_data)
            save_action_done(unique_id, 'load_followers')
            print(f"Followers data for {unique_id}: {followers_data}")
