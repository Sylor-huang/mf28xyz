#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-5-3 下午7:39
# @Author  : Sylor
# @File    : mf_text.py
# @Software: PyCharm
from bs4 import BeautifulSoup
import requests
from lxml import etree
from multiprocessing import Pool

def index_html(html):
    links = BeautifulSoup(html.text,'lxml').select('body > div.container > div > div.col-xs-12.col-sm-12.col-md-10 > div.container-fluid.novel_list > div.row > a')
    titles = BeautifulSoup(html.text,'lxml').select('body > div.container > div > div.col-xs-12.col-sm-12.col-md-10 > div.container-fluid.novel_list > div.row > a > div.pull-left')
    for title,link in zip(titles,links):
        data = {
            'title':title.get_text(),
            'link':link['href']
        }
        parse_html(data)


def parse_html(data):
    name = data['title']

    link = 'http://www.mf28.xyz' + data['link']
    text_html = response(link)
    content = etree.HTML(text_html.text).xpath("/html/body/div[3]/div/div[2]/text()")
    for text in content:
        print('开始保存文件')
        with open('/opt/xx/'+name+'.txt','w') as f:
            f.write(text)
            f.close()


def response(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response
        else:
            return None

    except:
        return None

def page(html):
    pagination = BeautifulSoup(html.text, 'lxml').find(title="下一页")
    if pagination:
        page_url = 'http://www.mf28.xyz' + pagination['href']
        return page_url
    else:
        return None



def main(url):
    while True:

        html = response(url)
        index_html(html)
        if page(html)==None:
            print('meiyou')
            break

        else:
            url = page(html)
            main(url)

if __name__ == '__main__':
    url = 'http://www.mf28.xyz/nlist_1_0.html'
    main(url)
    pool = Pool(10)
    pool.apply_async(main, index_html, parse_html, page)
    pool.close()
    pool.join()

