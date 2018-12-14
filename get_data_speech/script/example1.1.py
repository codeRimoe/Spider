# -*- coding: utf-8 -*-

# Get POI from Baidu Map Place API
# coding: utf-8
# PEP-8 standard
# Edit by Yue Luo: yue.rimoe@gmail.com
# http://rimoe.xyz
# reference： https://blog.csdn.net/WenWu_Both/article/details/70187605

# %%
import urllib2
import json
import time
import codecs

# %%
left_bottom = [112.5, 22.5]       # 设置区域左下角坐标（百度坐标系）
right_top = [113.5, 23.5]     # 设置区域右上角坐标（百度坐标系）
part_n = 2                    # 设置区域网格（2*2）

url0 = 'http://api.map.baidu.com/place/v2/search?'
x_item = (right_top[0] - left_bottom[0]) / part_n
y_item = (right_top[1] - left_bottom[1]) / part_n
query = '公园'                            # search key
ak = 'KdaepgQwpVfDNBCd9ZdTPhQhrT7mnicb'  # the AK of Baidu Map

n = 0
_t = []
for i in range(part_n):
    for j in range(part_n):
        # get the coordinate of left_bottom and right top
        lb_part = [left_bottom[0] + i * x_item, left_bottom[1] + j * y_item]
        rt_part = [lb_part[0] + x_item, lb_part[1] + y_item]
        for k in range(2):
            url = (url0 + 'query=' + query + '&page_size=20&page_num=' +
                   str(k) + '&scope=1&bounds=' + str(lb_part[1]) + ',' +
                   str(lb_part[0]) + ','+str(rt_part[1]) + ',' +
                   str(rt_part[0]) + '&output=json&ak=' + ak)
            print url
            data = urllib2.urlopen(url)
            hjson = json.loads(data.read())
            if hjson['message'] == 'ok':
                results = hjson['results']
                for m in range(len(results)):
                    for ii in results[m]:
                        _t.append(results[m])
        time.sleep(5)
        n += 1
        print '第%s个切片获取成功:%s' % (n, len(_t))

# %%

with codecs.open('C:/Users/Yue/Desktop/park.csv', 'w', 'utf-8') as wf:
    for i in _t:
        _tt = [i[u'name'],
               str(i[u'detail']),
               str(i[u'location'][u'lat']),
               str(i[u'location'][u'lng']),
               i[u'address'],
               i[u'uid']]
        wf.write(','.join(_tt)+'\n')
