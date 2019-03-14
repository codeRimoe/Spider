# -*- coding:utf-8 -*-

# Get the name and url of School (Department) in SYSU
# coding: utf-8
# PEP-8 standard
# Edit by Yue Luo: yue.rimoe@gmail.com
# https://blog.rimoe.xyz

# %%
import urllib2
import requests

import re
from bs4 import BeautifulSoup as bs

url = 'http://sysu.edu.cn/2012/cn/jgsz/yx/index.htm'

ctn = urllib2.urlopen(url)
txt = ctn.read()

pattern = re.compile(r'<a target="_blank" href="(.*?)">(.*?)</a>')
items = re.findall(pattern, txt)

soup = bs(txt, 'lxml')
items2 = soup.select('td')
for i in items2:
    try:
        print i.get_text(), i.a.attrs['href']
    except:
        print i.get_text()
