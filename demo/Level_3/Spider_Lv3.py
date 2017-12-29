# -*- coding: utf-8 -*-

# Spider Lv3
# Author: Yue H.W. Luo
# Mail: yue.rimoe@gmail.com
# License : http://www.apache.org/licenses/LICENSE-2.0
# More detial: http://blog.rimoe.ml/2017/11/12/post01/

"""
## NOTE
   Created on Thu Oct 26 15:30:04 2017
   This programme is used to get data from cnik-database.
   `threading`, `selenium` and `requests` module is needed.

## Reference:
   > http://cuiqingcai.com/2599.html
   > http://cuiqingcai.com/2621.html

===============================================================================

  rimoerimoerimoe     sysu       sysu     rimoerimoerimoe     sysu       sysu
  rimoerimoerimoe     sysu       sysu     rimoerimoerimoe     sysu       sysu
  yue                 sysu       sysu     yue                 sysu       sysu
  yue                  sysu     sysu      yue                 sysu       sysu
  rimoerimoerimoe       sysu   sysu       rimoerimoerimoe     sysu       sysu
  rimoerimoerimoe        sysu sysu        rimoerimoerimoe     sysu       sysu
              yue          rimoe                      yue     sysu       sysu
              yue          rimoe                      yue     sysu       sysu
              yue          rimoe                      yue     sysu       sysu
  rimoerimoerimoe          rimoe          rimoerimoerimoe     rimoerimoerimoe
  rimoerimoerimoe          rimoe          rimoerimoerimoe     rimoerimoerimoe
  
===============================================================================

93rd Anniversary,
Happy birthday!

"""

import re
import time
import requests
import threading
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException


class Spider:

    def __init__(self, dp, url):
        self.data_path = dp
        self.url = url
        self.dlist = []
        self.html = ''
        self.string = ''
        self.todo = ['申请号', '申请日', '公开号', '公开日', '申请人',
                     '地址', '共同申请人', '发明人', '国际申请', '国际公布',
                     '进入国家日期', '专利代理机构', '代理人', '分案原申请号',
                     '国省代码', '摘要', '主权项', '页数', '主分类号',
                     '专利分类号']
        self.driver = webdriver.Chrome()

    # Search: controling the webdriver via selenium
    def search(self, search_whe, search_key, search_type):
        driver = self.driver
        driver.get(self.url)
        time.sleep(5)
        inbox = driver.find_element_by_xpath('//*[@id="Text1"]')
        buton = driver.find_element_by_xpath(
                '//*[@id="Table6"]/tbody/tr[1]/td[3]/table/tbody/tr/td/input')
        where = driver.find_element_by_xpath('//*[@id="Select1"]')
        pages = driver.find_element_by_xpath(
                '//*[@id="Table8"]/tbody/tr/td/select[3]')
        types = [
            driver.find_element_by_xpath('//*[@id="专利类别1"]'),   # 专利发明
            driver.find_element_by_xpath('//*[@id="专利类别2"]'),   # 外观设计
            driver.find_element_by_xpath('//*[@id="专利类别3"]')    # 实用新型
        ]
        inbox.clear()
        inbox.send_keys(search_key)
        for t in types:
            t.click()
        types[search_type].click()
        Select(pages).select_by_value('50')
        Select(where).select_by_value(search_whe)
        time.sleep(5)
        buton.click()

    # Get url: get the url list
    def get_site(self):
        driver = self.driver
        try:
            next = driver.find_element_by_xpath(
                    '//*[@id="id_grid_turnpage2"]/a[1]')
        except NoSuchElementException:
            global search_whe, search_key, search_type
            time.sleep(5)
            self.search(search_whe, search_key, search_type)
        pattern = re.compile(r'(.*?)&QueryID=\d+&CurRec=\d')
        while 1:
            i = 1
            while 1:
                i += 1
                try:
                    a = driver.find_element_by_xpath(
                        '//*[@id="contentBox"]/table/tbody/tr[%s]/td[2]/a' % i)
                except:
                    break
                txt = a.get_attribute("href")
                txt = re.findall(pattern, txt)[0]
                self.dlist.append(txt)
                print('Thread 1: ' + txt)
            next.click()
            next = driver.find_element_by_xpath(
                    '//*[@id="id_grid_turnpage2"]/a[3]')
        self.close()

    # Get the infomation
    def get_data(self):
        save_name = 'save.txt'
        with open(self.data_path + '\\' + save_name, 'a') as sf:
            self.string = '名称,' + ','.join(self.todo)
            sf.write(self.string + '\n')
        while 1:
            try:
                p = self.dlist.pop(0)
            except IndexError:
                print('Thread 2: ' + 'List has noting.')
                time.sleep(2)
                continue
            self.html = requests.get(p).text.encode('utf-8')
            with open(self.data_path + '\\' + save_name, 'a') as sf:
                self.analyse()
                print('Thread 2: ' + self.string)
                sf.write(self.string + '\n')

    # Get each record by using regular expressions
    def get_(self, pattern):
        pattern = re.compile(r'【' + pattern + '】.*?nbsp;(.*?)<', re.S)
        try:
            s = re.findall(pattern, self.html)[0]
            s = s.replace('\r', '').replace('\n', '').replace('\t', '')
            self.string += '"' + s + '",'
        except IndexError:
            self.string += ' ,'

    def analyse(self):
        pattern = re.compile(r'<title>(.*?)--', re.S)
        try:
            self.string = re.findall(pattern, self.html)[0] + ','
        except IndexError:
            self.string = ' ,'
        for i in self.todo:
            self.get_(i)
        self.string.strip(',')

    def close(self):
        self.driver.close()


data_path = r'C:\Users\Jack\Desktop'
search_whe = u'地址'
search_key = u'东莞'
search_type = 0
url = 'http://dbpub.cnki.net/grid2008/dbpub/brief.aspx?id=scpd'


spider = Spider(data_path, url)
spider.search(search_whe, search_key, search_type)

threads = []
t1 = threading.Thread(target=spider.get_site, args=())
threads.append(t1)
t2 = threading.Thread(target=spider.get_data, args=())
threads.append(t2)

for t in threads:
    t.setDaemon(True)
    t.start()
