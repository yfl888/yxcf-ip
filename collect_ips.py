import requests
from bs4 import BeautifulSoup
import re
import ipaddress

# 目标 URL 列表（可添加更多）
urls = [
    'https://api.uouin.com/cloudflare.html',
    'https://ip.164746.xyz',
    'https://addressesapi.090227.xyz/cmcc-ipv6'
]

# 正则匹配
ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
ipv6_pattern = r'\b(?:[A-Fa-f0-9]{0,4}:){2,7}[A-Fa-f0-9]{0,4}\b'

# 检查ipv4.txt, ipv6.txt文件是否存在,如果存在则删除它
for file_name in ['ipv4.txt', 'ipv6.txt']:
    if os.path.exists(file_name):
        os.remove(file_name)

print("[INFO] 开始抓取 Cloudflare IP ...")

# IP 校验函数
def is_valid_ip(ip, version):
    try:
        return ipaddress.ip_address(ip).version == version
    except ValueError:
        return False

# 抓取并提取
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
        # 提取 IPv4
        ipv4_matches = re.findall(ipv4_pattern, text)
        for ip in ipv4_matches:
            if is_valid_ip(ip, 4):
                ipv4_set.add(ip.strip())

        # 提取 IPv6
        ipv6_matches = re.findall(ipv6_pattern, text)
        for ip in ipv6_matches:
            if is_valid_ip(ip, 6):
                ipv6_set.add(ip.strip())

# 去重集合
ipv4_set = set()
ipv6_set = set()

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
