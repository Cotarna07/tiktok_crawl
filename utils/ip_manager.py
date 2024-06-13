import json
import subprocess
import psutil
import time
# v2rayN 配置文件路径
config_path = r"D:\softwear\v2rayN-With-Core\guiConfigs\config.json"

def switch_ip(ip):
    print(f"Switching to IP: {ip}")
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = json.load(file)
        config['outbounds'][0]['settings']['vnext'][0]['address'] = ip
        with open(config_path, 'w', encoding='utf-8') as file:
            json.dump(config, file, ensure_ascii=False, indent=4)
        print(f"IP switched to {ip} in config file.")
    except Exception as e:
        print(f"Error switching IP in config file: {e}")

def restart_v2rayn():
    # 关闭 v2rayN
    for proc in psutil.process_iter():
        if proc.name() == "v2rayN.exe":
            proc.kill()

    # 清除DNS缓存
    subprocess.run(['ipconfig', '/flushdns'])
    
    # 重启 v2rayN
    subprocess.Popen([r"D:\softwear\v2rayN-With-Core\v2rayN.exe"])

def check_vpn_connection():
    try:
        # 尝试访问一个公共网站
        response = subprocess.check_output(['ping', '-n', '1', '8.8.8.8'])
        return 'TTL' in str(response)
    except subprocess.CalledProcessError:
        return False

def monitor_vpn():
    while True:
        if not check_vpn_connection():
            print("VPN disconnected, restarting...")
            restart_v2rayn()
        else:
            print("VPN is connected.")
        time.sleep(300)  # 每5分钟检查一次

# 示例代码（可选，用于测试）
if __name__ == "__main__":
    monitor_vpn()  # 开始监控VPN连接
