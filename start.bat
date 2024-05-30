@echo off
echo Select an action to perform:
echo 1. Scroll and load all videos
echo 2. Get follower list
echo 3. Download videos

set /p action="Enter your choice (1, 2, or 3): "

C:\Users\ASUSA\AppData\Local\Programs\Python\Python311\python.exe D:\software\tiktok_crawl\main.py %action%
pause
