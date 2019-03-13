# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 19:07:03 2019

@author: Yue
"""

import os
import time
import json
import urllib2

os.chdir('data')
# key of Tencent map api
keys = ['K24BZ-SSSSS-YYYYY-SSSSS-UUUUU-23333',
        'DK6BZ-SSSSS-YYYYY-SSSSS-UUUUU-23333',
        'ZDSBZ-SSSSS-YYYYY-SSSSS-UUUUU-23333',
        'PVPBZ-SSSSS-YYYYY-SSSSS-UUUUU-23333',
        'E35BZ-SSSSS-YYYYY-SSSSS-UUUUU-23333']
url = 'https://apis.map.qq.com/ws/streetview/v1/getpano?location' +\
      '={},{}&radius=100&key={}'

done_record = 0
i = 0
done = []
not_ok = []

# X/Y:GCJ02, X_/Y_:WGS84
with open('listnew.csv', 'r') as rf:
    for line in rf:
        if i < done_record:
            continue
        row = line.strip().split(',')
        web = urllib2.urlopen(url.format(row[3], row[2], keys[i % 5]))
        data = web.read()
        data = json.loads(data)
        if data['status'] == 0:
            # save valid data
            done.append(data)
            print("done %s" % len(done))
        elif data['status'] == 346:
            # pass if no street view data
            print("data pass%s" % i)
        else:
            # error log
            not_ok.append([row[3], row[2], data['status']])
            print("error %s" % data['status'])
        i += 1
        time.sleep(0.2)
with open('meta_raw_done.json', 'w') as wf:
    json.dump(done, wf)
with open('meta_raw_not_ok.json', 'w') as wf:
    json.dump(not_ok, wf)

# %%
# data clean: del same svid and make a list
# import os
# import json

clean = {}

# with open('meta_raw_done.json', 'r') as rf:
#     raw = json.load(rf)
raw = done

for r in raw:
    r = r['detail']
    _tmp = r['location']
    clean[r['id']] = [_tmp['lng'], _tmp['lat']]

with open('all_img_list_gcj.csv', 'w') as wf:
    for c in clean:
        wf.write(','.join([c, str(clean[c][0]), str(clean[c][1])]) + '\n')
