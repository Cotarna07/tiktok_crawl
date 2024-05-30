import subprocess
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def start_browser():
    subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--remote-debugging-port=9222"])
    time.sleep(5)

    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=options)
    return driver

def schedule_tasks(tasks, interval):
    random.shuffle(tasks)
    for task in tasks:
        task()
        time.sleep(interval)

def run_scheduler(task_list, interval=2400):
    schedule_tasks(task_list, interval)
