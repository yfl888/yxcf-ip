import requests
from bs4 import BeautifulSoup
import re
import os
import time

# 目标URL列表
urls = [
    'https://api.uouin.com/cloudflare.html',
    'https://ip.164746.xyz'
]

# IPv4 和 IPv6 正则表达式
ipv4_pattern = r'(?:\d{1,3}\.){3}\d{1,3}'
ipv6_pattern = r'(?:[A-Fa-f0-9]{1,4}:){1,7}[A-Fa-f0-9]{1,4}'
ip_pattern = rf'{ipv4_pattern}|{ipv6_pattern}'

# 存储IP集合
ipv4_set = set()
ipv6_set = set()

for url in urls:
    try:
        # 加随机参数防缓存
        response = requests.get(url, params={"_t": int(time.time())}, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[错误] 无法访问 {url} - {e}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all(['tr', 'li'])

    for element in elements:
        element_text = element.get_text()
        ip_matches = re.findall(ip_pattern, element_text)

        for ip in ip_matches:
            if re.fullmatch(ipv4_pattern, ip):
                ipv4_set.add(ip)
            elif re.fullmatch(ipv6_pattern, ip):
                ipv6_set.add(ip)

# 保存并检测变化
def save_and_check(filename, new_ips):
    old_ips = set()
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            old_ips = set(line.strip() for line in f if line.strip())

    if new_ips != old_ips:
        with open(filename, 'w') as f:
            for ip in sorted(new_ips):
                f.write(ip + '\n')
        print(f"[更新] {filename} 已更新，共 {len(new_ips)} 个 IP")
    else:
        print(f"[无变化] {filename} 内容未变")

save_and_check('ipv4.txt', ipv4_set)
save_and_check('ipv6.txt', ipv6_set)
