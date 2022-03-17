from optparse import OptionParser
from json.tool import main
import requests
from tqdm import tqdm
from requests import RequestException
from lxml import etree
from contextlib import closing
from pyquery import PyQuery as pq
import cowsay
import re
import os
import sys
import json
import urllib3
import subprocess
urllib3.disable_warnings()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
}


def get_media(ops):
    baseurl = ops.url
    html = requests.get(url=baseurl, headers=headers).text
    sum=0
    doc = pq(html)
    title = doc('#viewbox_report > h1 > span').text()
    pattern = r'\<script\>window\.__playinfo__=(.*?)\</script\>'
    result = re.findall(pattern, html)[0]
    temp = json.loads(result)
    url = temp["data"]["dash"]["video"][0]['baseUrl']

    print("\n")
    print(("---开始下载视频---")+title)
    headers.update({'Referer': baseurl})
    res = requests.Session()
    begin = 0
    end = 1024*1024 - 1
    flag = 0

    filename = "./"+title+".flv"


    while True:
        headers.update({'Range': 'bytes=' + str(begin) + '-' + str(end)})
        res = requests.get(url=url, headers=headers, verify=False)
        if res.status_code != 416:
            begin = end + 1
            end = end + 1024*1024
            pbar = tqdm(total=int(res.headers['Content-Range'].split('/')[1]), ncols=80)
        else:
            headers.update({'Range': str(end + 1) + '-'})
            res = requests.get(url=url, headers=headers, verify=False)
            flag = 1
        with open(filename, 'ab') as fp:
            fp.write(res.content)
            sum = sum+1024*1024
            pbar.update(sum)
            fp.flush()
            pbar.close()
        
        if flag == 1:
            fp.close()
            break
    #print('---视频下载完成---')
    pbar.close()
    print('---开始下载音频---')
    filename = "./"+title+".mp3"
    url = temp["data"]["dash"]["audio"][0]['baseUrl']
    while True:
        headers.update({'Range': 'bytes=' + str(begin) + '-' + str(end)})
        res = requests.get(url=url, headers=headers, verify=False)
        if res.status_code != 416:
            begin = end + 1
            end = end + 1024*1024
        else:
            headers.update({'Range': str(end + 1) + '-'})
            res = requests.get(url=url, headers=headers, verify=False)
            flag = 1
            
        with open(filename, 'ab') as fp:
            fp.write(res.content)
        if flag == 1:
            fp.close()
            break


    com = f'.\\ffmpeg\\ffmpeg-master-latest-win64-gpl-shared\\bin\\ffmpeg.exe  -i "{title+".mp3"}" -i "{title+".flv"}"  ' \
        f'-acodec copy -vcodec copy "{title+".mp4"}" 1> log.txt 2>&1 '
    os.system(com)
    os.remove(title+".flv")
    
    if ops.file_type == "MV":
        os.remove(title+".mp3")
        print("视频合成成功")
    elif ops.file_type == "AU":
        os.remove(title+".mp4")
        print("音频下载成功")
    else:
        print("视频、音频文件下载成功")
        sys.exit(0)

def main():
    cowsay.cow('WELCOME TO BILIBILI_SPIDER')
    parser = OptionParser('python bilispider.py -u <Target URL> -f <file_type> ')
    parser.add_option('-u',  dest='url', type='string', help='target url for download')
    parser.add_option('-f', dest='file_type', type='string', help='MV or AU or ALL')
    (options, args) = parser.parse_args()
    if options.url and options.file_type:
        get_media(options)
        sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
