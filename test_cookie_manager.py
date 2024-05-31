import json

def load_cookies(config_file_path):
    try:
        with open(config_file_path, 'r', encoding='utf-8') as file:
            config = json.load(file)
        return config['accounts'][0]['cookies']
    except Exception as e:
        print(f"Error loading cookies: {e}")
        return []

def update_browser_cookies(driver, cookies):
    print("Updating browser cookies...")
    driver.delete_all_cookies()
    for cookie in cookies:
        if 'expirationDate' in cookie:
            cookie['expiry'] = int(cookie['expirationDate'])
        if 'sameSite' in cookie and cookie['sameSite'] not in ["Strict", "Lax", "None"]:
            del cookie['sameSite']
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"Error adding cookie: {e}")

def save_last_processed_user(last_processed_user_file, unique_id):
    try:
        with open(last_processed_user_file, 'w', encoding='utf-8') as file:
            json.dump({"last_processed_user": unique_id}, file)
    except Exception as e:
        print(f"Error saving last processed user: {e}")

def load_last_processed_user(last_processed_user_file):
    try:
        with open(last_processed_user_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data.get("last_processed_user", None)
    except Exception as e:
        print(f"Error loading last processed user: {e}")
        return None

def save_cookies(driver, file_path):
    cookies = driver.get_cookies()
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(cookies, file)