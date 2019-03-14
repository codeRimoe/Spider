# -*- coding: utf-8 -*-

# Spider Lv1
# Author: Yue H.W. Luo
# Mail: yue.rimoe@gmail.com
# License : http://www.apache.org/licenses/LICENSE-2.0
# More detial: https://blog.rimoe.xyz/2017/08/24/post01/

import urllib2
import re

res = urllib2.urlopen("http://rimoe.ml")        # 打开网页http://rimoe.ml

txt1 = res.read()
pattern1 = re.compile(r'<li>(.*?)</li>', re.S)  # 提取列表标签<li>
txt2 = re.findall(pattern1, txt1)
pattern2 = re.compile(r'<a.*?href=(.*?)>(.*?)</a>', re.S)

with open('data.txt', 'w') as file:
    for txt in txt2:
        results = re.findall(pattern2, txt)     # 逐项提取链接标签<a>
        file.write('Project:')                  # 格式化输出
        for result in results:
            file.write('\n'+result[1] + ':' + result[0])
        file.write('\n\n')
