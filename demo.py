#!/usr/bin/python
# -*- coding: UTF-8 -*-
from downloader import dl_album,dl_song,dl_plist
from requests.packages import urllib3
import json
import os
import platform as pf
import shutil

# Three_Party_Lib:requests,mutagen


# disable ssl warning:
urllib3.disable_warnings()

curdir = os.path.dirname(__file__)

if pf.system() == 'Linux' or pf.system() == 'Darwin':
    pfile_path = os.path.join(os.environ['HOME'],'.config/musec/setting.json')
elif pf.system() == 'Windows':
    pfile_path = os.path.join(os.environ['APPDATA'],'musec\\setting.json')


if not os.path.exists(pfile_path):
    if not os.path.exists(os.path.split(pfile_path)[0]):
        os.makedirs(os.path.split(pfile_path)[0])
    shutil.copyfile('config/setting.json',pfile_path)

with open(pfile_path) as profile:
    setting = json.load(profile)


path     = setting['donwload_path']
sformat  = setting['download_format']
info     = setting['download_info']
errcha   = setting['error_cha']
uin      = setting['uin']

platform = setting['platform']
if platform == 'Auto':
    platform = pf.system()


# cookies:
cookies_str = ''

# load cookies from strings like this: 'aaa=bbb; ccc=ddd....'
if cookies_str:
    cookies = {}
    for line in cookies_str.split(';'):
        name,value=line.strip().split('=',1)
        cookies[name]=value  

# load cookies if exist cookies.json
elif os.path.exists('config/cookies.json'):
    with open('config/cookies.json') as f:
        cookies = json.load(f)





#dl_song(mid, path, platform, info, uin, cookies, errcha, sformat)

# ct:Start to download from ct
#dl_album(mid, path, platform, info, uin, cookies, errcha, sformat, ct=0)
#dl_plist(mid, path, platform, info, uin, cookies, errcha, sformat, ct=0)
