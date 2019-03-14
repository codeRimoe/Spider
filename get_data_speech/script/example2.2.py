# -*- coding: utf-8 -*-

# Spider Lv2
# Author: Yue H.W. Luo
# Mail: yue.rimoe@gmail.com
# License : http://www.apache.org/licenses/LICENSE-2.0
# More detial: https://blog.rimoe.xyz/2017/09/04/post01/

import sys
import urllib2
import re
import json
from bs4 import BeautifulSoup as bs
from imghdr import what

reload(sys)
sys.setdefaultencoding('utf-8')


save_dir = '/Users/_nA/Desktop/data/'    # 存储路径
cookie = 'SINAGLOBAL=balabala'           # 输入cookie
headers = {'cookie': cookie}


def get_res(page, headers):
    url = ('http://weibo.com/u/3803639941?is_search=0&visible=0&'
           'is_all=1&is_tag=0&profile_ftype=1&page=%d') % page
    request = urllib2.Request(url, headers=headers)
    # 将URL、Header打包请求，当然这里还可以有别的参数
    # class urllib2.Request(url[, data][, headers]\
    # [, origin_req_host][, unverifiable])

    response = urllib2.urlopen(request)
    # 提交请求并获取响应

    html = response.read()
    pattern = re.compile((r'"domid":"Pl_Official_MyProfileFeed__22"'
                          ',(.*?)\)</script>'), re.S)
    webres = re.findall(pattern, html)[0]  # 用正则表达式提取包含内容部分
    webres_json = json.loads('{'+webres)  # 解析json字符串，前面要补充`{`字符
    webres_html = webres_json['html']
    return webres_html


def save_data(webres_html, save_dir):
    # 使用BeautifulSoup对webres_html进行分析
    soup = bs(webres_html, 'lxml')  # 构建Soup
    infos = soup.find_all(class_="WB_detail")
    pattern_pic = re.compile(r'pic_id=(.*)')
    dataid = 1

    with open(save_dir+'/infos.txt', 'a') as txt_f:
        for info in infos:
            Stxt = ""
            try:
                txts = info.find_all(class_="WB_text W_f14")[0].contents
                pics = info.find_all('li')
                for txt in txts:
                    try:
                        for txtc in txt.contents:
                            Stxt += txtc              # 对于链接文本，提取其内容
                    except:
                        Stxt += txt                   # 否则原样输出
                for pic in pics:                      # 得到图片URL
                    picid = re.findall(pattern_pic, pic.get('action-data'))[0]
                    pic_url = "http://wx1.sinaimg.cn/mw690/" + picid + '.jpg'
                    photo = urllib2.urlopen(pic_url).read()
                    pic_type = what('', h=photo)     # 判断图片格式
                    if not pic_type:                 # 若无法识别格式返回None
                        pic_type = ''
                    name = (save_dir + str(page) + '_' +
                            str(dataid) + '_' + picid + '.' + pic_type)
                    print name + ',' + pic_url
                    with open(name, 'wb') as f:
                        f.write(photo)
            except:
                pass
            print Stxt
            txt_f.write(str(page) + '_' + str(dataid) +
                        ' : ' + Stxt.decode('utf-8') + '\n')
            dataid += 1

for page in range(1, 5):
    webres_html = get_res(page, headers)
    save_data(webres_html, save_dir)
