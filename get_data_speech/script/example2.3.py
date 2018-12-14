# -*- coding:utf-8 -*-

# Get the baidu Map POI
# coding: utf-8
# PEP-8 standard
# Edit by Yue Luo: yue.rimoe@gmail.com
# http://rimoe.xyz# -*- coding: utf-8 -*-

import codecs
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


city = u"佛山市"
poi_type = u"公园"

driver = webdriver.Chrome()
driver.get('https://map.baidu.com/')

city_change = driver.find_element_by_xpath('//*[@id="ui3_city_change"]/a')
city_change.click()
time.sleep(0.5)
city_inbox = driver.find_element_by_xpath('//*[@id="selCityCityWd"]')
city_inbox.clear()
city_inbox.send_keys(city)
time.sleep(0.5)
city_search = driver.find_element_by_xpath('//*[@id="selCitySubmit"]')
city_search.click()
time.sleep(0.5)

inbox = driver.find_element_by_xpath('//*[@id="sole-input"]')       # 获取元素
inbox.clear()                                                  # 清空文本框内容
inbox.send_keys(poi_type)                                 # 在已有内容后添加文本
search = driver.find_element_by_xpath('//*[@id="search-button"]')
search.click()
time.sleep(0.5)

pois = []
page = 0

while 1:
    poi_links = driver.find_elements_by_xpath(
                '//*[@data-stat-code="poisearch.scenery.title"]')
    time.sleep(0.5)
    for poi_link in poi_links:
        time.sleep(0.5)
        poi_link.click()
        time.sleep(1)
        poi = []
        feature_list = [
                '//*[@id="generalheader"]/div[1]/div[1]/span',     # 名称
                '//*[@id="generalheader"]/div[1]/div[2]/span[1]',  # 评分
                '//*[@id="generalinfo"]/div[2]/div/span[2]',       # 地址
                '//*[@class="c-main c-color-auxi"]',               # 评论
                '//*[@class="special23-right-item"]/span',         # 营业时间
                '//*[@class="special21-introduce BMap-log"]',      # 简介
                '//*[@class="special21-overflow"]',                # 建议游玩
                ]
        for f in feature_list:
            try:
                print driver.find_element_by_xpath(f).text
                poi.append(driver.find_element_by_xpath(f).text)
            except:
                poi.append(' ')
        try:
            poi.append('|'.join(
                    [x.text for x in driver.find_elements_by_xpath(
                       '//*[@class="labels-inner c-color-red c-abstract"]/span'
                       )]))
            poi.append('|||'.join(
                    [x.text for x in driver.find_elements_by_xpath(
                       '//*[@class="comment-cont J-commit-content BMap-log"]'
                       )]))
        except:
            poi.append(' ')
        pois.append('\t'.join(poi))
        time.sleep(0.5)
        driver.find_element_by_xpath(
                '//*[@class="card status-return fold"]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@tid="toNextPage"]').click()

    time.sleep(0.5)
    ActionChains(driver).move_to_element(driver.find_element_by_xpath(
                '//*[@class="card status-fold fold"]').click()).perform()
    time.sleep(1.5)
    if page > 4:
        break
    else:
        page += 1

driver.close()                        # 关闭webdriver
with codecs.open('C:/Users/Yue/Desktop/pois.txt', 'w', 'utf-8') as wf:
    wf.write(u'名称\t评分\t地址\t评论\t时间\t简介绍\t游玩\t评论\n')
    wf.write('\n'.join(pois))
