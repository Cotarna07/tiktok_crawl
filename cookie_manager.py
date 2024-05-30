# cookie_manager.py

import json

def load_config(config_file_path):
    with open(config_file_path, 'r') as file:
        return json.load(file)

def save_config(config_file_path, config):
    with open(config_file_path, 'w') as file:
        json.dump(config, file, indent=4)

def update_browser_cookies(driver, cookies):
    driver.delete_all_cookies()
    for cookie in cookies:
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry'])
        if 'sameSite' in cookie and cookie['sameSite'] not in ["Strict", "Lax", "None"]:
            del cookie['sameSite']
        driver.add_cookie(cookie)

def manage_cookies(driver, config_file_path, account_name=None, save=False):
    config = load_config(config_file_path)
    current_account_index = config.get('current_account_index', 0)
    accounts = config['accounts']
    current_account = accounts[current_account_index]

    if save:
        updated_cookies = driver.get_cookies()
        for account in accounts:
            if account['username'] == account_name:
                account['cookies'] = updated_cookies
                break
        config['current_account_index'] = (current_account_index + 1) % len(accounts)
        save_config(config_file_path, config)
    else:
        update_browser_cookies(driver, current_account['cookies'])
        config['current_account_index'] = (current_account_index + 1) % len(accounts)
        save_config(config_file_path, config)

def switch_account(driver, config_file_path):
    manage_cookies(driver, config_file_path, save=True)
    manage_cookies(driver, config_file_path)
