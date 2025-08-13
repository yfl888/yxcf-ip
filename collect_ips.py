import requests
from bs4 import BeautifulSoup
import re
import os

# 目标 URL 列表（可以继续添加）
urls = [
    'https://api.uouin.com/cloudflare.html',
    'https://ip.164746.xyz'
]

# 正则：IPv4 和 IPv6
ipv4_pattern = r'\b\d{1,3}(?:\.\d{1,3}){3}\b'
ipv6_pattern = r'\b(?:[0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}\b'

ipv4_set = set()
ipv6_set = set()

print("[INFO] 开始抓取 Cloudflare IP ...")

for url in urls:
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"[ERROR] 无法访问 {url} - {e}")
        continue

    soup = BeautifulSoup(resp.text, 'html.parser')
    elements = soup.find_all(['tr', 'li', 'p', 'span', 'div'])

    for element in elements:
        text = element.get_text()
        ipv4_matches = re.findall(ipv4_pattern, text)
        ipv6_matches = re.findall(ipv6_pattern, text)

        for ip in ipv4_matches:
            ipv4_set.add(ip.strip())
        for ip in ipv6_matches:
            # 过滤掉短 IPv6（如 ::1）
            if ":" in ip and len(ip) > 6:
                ipv6_set.add(ip.strip())

# 保存 IPv4
with open('ipv4.txt', 'w') as f4:
    for ip in sorted(ipv4_set):
        f4.write(ip + '\n')

# 保存 IPv6
with open('ipv6.txt', 'w') as f6:
    for ip in sorted(ipv6_set):
        f6.write(ip + '\n')

print(f"[DONE] 共获取 IPv4: {len(ipv4_set)} 个, IPv6: {len(ipv6_set)} 个")
print("文件已生成：ipv4.txt, ipv6.txt")

