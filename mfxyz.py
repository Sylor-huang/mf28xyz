#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-4-30 上午11:42
# @Author  : Sylor
# @File    : mfxyz.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import os
from multiprocessing import Pool

def html_index(html):
    soup = BeautifulSoup(html.text,'lxml')
    lists = soup.select('.list')
    for li in lists:
        titles = li.select('.title')[0].get_text()
        srcs = [img.attrs['data-original'] for img in li.select('.img')]
        data = {
            titles:srcs
        }
        for title,src in data.items():
            img_name = '{}'.format(title)
            mkdir(img_name)
            print('创建文件夹',img_name)
            for img_url in src:
                print('开始保存图片')
                html_parse(img_url)

def html_parse(img_url):
    name = img_url[-10:-4]
    img_a = response(img_url)
    f = open(name + '.jpg','ab')
    f.write(img_a.content)
    f.close()

#
#
#
#
def mkdir(img_name, isExists=None):
    path = img_name.strip()
    if not isExists:
        print('建了一个名字叫',path,'的文件夹')
        os.makedirs(os.path.join("/opt/meinv2",path))
        os.chdir(os.path.join("/opt/meinv2/"+path))
        return True
    else:
        print('名字叫',path,'的文件夹已存在')
        return False


def response(url):
    try:
        content = requests.get(url)
        if content.status_code == 200:
            return content
        else:
            pass
    except RequestException:
        return None


def main(i):
    while i < 1000:
        url = 'http://www.mf28.xyz/imglist_31_'+str(i)+'.html'
        html = response(url)
        html_index(html)
    else:
        print('已到最后一页')


if __name__ == '__main__':
    pool = Pool(10)
    pool.map(main,[i for i in range (0,1000)])

    pool.close()
    pool.join()