import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = ['https://api.uouin.com/cloudflare.html', 
        'https://ip.164746.xyz'
        ]

# 正则表达式用于匹配IPv4地址
ipv4_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 正则表达式用于匹配IPv6地址
ipv6_pattern = r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b'

# 检查ip.txt文件是否存在,如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 创建一个文件来存储IP地址
with open('ip.txt', 'w') as file:
    for url in urls:
        # 发送HTTP请求获取网页内容
        response = requests.get(url)
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 根据网站的不同结构找到包含IP地址的元素
        if url == 'https://api.uouin.com/cloudflare.html':
            elements = soup.find_all('tr')
        elif url == 'https://ip.164746.xyz':
            elements = soup.find_all('tr')
        else:
            elements = soup.find_all('li')
        
        # 遍历所有元素,查找IP地址
        for element in elements:
            element_text = element.get_text()
            
            # 查找IPv4地址
            ipv4_matches = re.findall(ipv4_pattern, element_text)
            for ipv4 in ipv4_matches:
                file.write(ipv4 + '\n')
            
            # 查找IPv6地址
            ipv6_matches = re.findall(ipv6_pattern, element_text)
            for ipv6 in ipv6_matches:
                file.write(ipv6 + '\n')

print('IP地址已保存到ip.txt文件中。')
