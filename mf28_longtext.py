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
    links = BeautifulSoup(html.text,'lxml').select('div.col-xs-12.col-sm-12.col-md-10 > div.container-fluid.novel_list > a')
    titles = BeautifulSoup(html.text,'lxml').find_all('div',style='font-size:18px; color:#000; overflow: hidden; white-space:nowrap; text-overflow:ellipsis; line-height:200%')
    # titles = etree.HTML(html.text).xpath("/html/body/div[3]/div/div[2]/div[6]/a/div[1]/text()")
    # print(titles)     #用xapth也可以提取

    for title,link in zip(titles,links):
        data = {
            'title':title.get_text(),
            'link':link['href']
        }
        parse_html(data)


def parse_html(data):
    page_index = 'http://www.mf28.xyz' + data['link']
    page_html = response(page_index)
    page_parse = BeautifulSoup(page_html.text,'lxml').find('div',style="border: 1px solid #ccc; padding: 15px 15px; text-align: center;").find_all('a')
    name = data['title']
    for a in page_parse:
        txt_index = 'http://www.mf28.xyz/' + a['href']
        txt_html = response(txt_index)
        txt_content = etree.HTML(txt_html.text).xpath('/html/body/div[3]/div/div[2]/text()')
        print('开始写入文本',name)
        for txt in txt_content:
            with open('/opt/wxx/'+name+'.txt','a') as f:  # a 的方式写入是追加到后面的，不会覆盖前面的内容，或者w模式下将f.close()移到with平起的位置，这样多次写入也不会覆盖前面的内容。
                f.write(txt)
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
            break

        else:
            url = page(html)
            main(url)

if __name__ == '__main__':
    url = 'http://www.mf28.xyz/lnlist_2_0.html'
    main(url)
    pool = Pool(10)
    pool.apply_async(main, index_html, parse_html, page)
    pool.close()
    pool.join()

