import requests

def get_ip(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP: {e}")
        return None

def main():
    # 获取IPv4地址
    ipv4_url = 'https://api.ipify.org'
    ipv4 = get_ip(ipv4_url)
    
    # 获取IPv6地址
    ipv6_url = 'https://api64.ipify.org'
    ipv6 = get_ip(ipv6_url)

    # 更新ip.txt
    with open("ip.txt", "w") as file:
        if ipv4:
            file.write(f"IPv4: {ipv4}\n")
        if ipv6:
            file.write(f"IPv6: {ipv6}\n")
    
    print("IP addresses updated in ip.txt")

if __name__ == "__main__":
    main()
