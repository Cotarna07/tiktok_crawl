import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService

def kill_processes(process_name):
    try:
        subprocess.run(f'taskkill /F /IM {process_name}.exe', shell=True)
        print(f"Killed all {process_name} processes.")
    except Exception as e:
        print(f"Error killing {process_name} processes: {e}")

def start_chrome_browser():
    subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--remote-debugging-port=9222"])
    time.sleep(5)

    options = ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=options)
    return driver

def start_edge_browser():
    try:
        kill_processes('msedge')
        subprocess.Popen([r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", "--remote-debugging-port=9223"])
        time.sleep(10)

        edge_options = EdgeOptions()
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--no-sandbox")
        edge_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")

        service = EdgeService(verbose=True)
        driver = webdriver.Edge(service=service, options=edge_options)
        return driver
    except Exception as e:
        print(f"Error starting Edge browser: {e}")
        return None

def start_firefox_browser():
    try:
        firefox_path = r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
        geckodriver_path = r"C:\Program Files (x86)\Mozilla Firefox\geckodriver.exe"
        subprocess.Popen([firefox_path, '-marionette'])
        time.sleep(5)

        firefox_service = FirefoxService(executable_path=geckodriver_path, service_args=['--marionette-port', '2828', '--connect-existing'])

        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--no-sandbox")

        driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
        return driver
    except Exception as e:
        print(f"Error starting Firefox browser: {e}")
        return None
