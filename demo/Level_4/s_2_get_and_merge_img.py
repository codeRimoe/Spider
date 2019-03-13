# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 21:24:23 2019

@author: Yue
"""
import os
import cv2
import json
import requests
import numpy as np

os.chdir(r'data')
rpath = 'raw_img'
mpath = 'meg_img'


def download(path, svid, x, y):
    # down street view image
    url = 'https://sv6.map.qq.com/tile?svid={}&x={}&y={}&level=0' +\
      '&mtype=mobile-cube&from=web'
    path = '{}/id{}_x{}_y{}.jpg'.format(path, svid, x, y)
    r = requests.get(url.format(svid, x, y))
    with open(path, 'wb') as fd:
        fd.write(r.content)


def merge_y(path, svid, x):
    # merge y axis
    img1 = cv2.imread('%s/id%s_x%s_y0.jpg' % (path, svid, x), 1)
    img2 = cv2.imread('%s/id%s_x%s_y1.jpg' % (path, svid, x), 1)
    if img1 is None:
        download(path, svid, x, 0)
    if img2 is None:
        download(path, svid, x, 1)
    try:
        return np.concatenate([img1, img2], axis=0)
    except ValueError:
        return merge_y(path, svid, x)


def merge_x(path, svid, n):
    # merge x axis
    x = 2 * n
    img1 = merge_y(path, svid, x)
    img2 = merge_y(path, svid, x + 1)
    return np.concatenate([img1, img2], axis=1)


# read todo list
with open('all_img_list_gcj.csv', 'r') as rf:
    rf.readline()
    clean = rf.readlines()

done = []
# with open('done_meg.json', 'r') as wf:
#    done = json.load(wf)

for svid in clean:
    svid = svid.split(',')[0]
    if svid in done:
        continue
    for n in range(4):
        _img = merge_x(rpath, svid, n)
        cv2.imwrite('%s/id%s_%s.jpg' % (mpath, svid, n), _img)
    done.append(svid)
    # save for interup
    print "done:%s_%s" % (svid, len(done))
    with open('done_meg.json', 'w') as wf:
        json.dump(done, wf)
