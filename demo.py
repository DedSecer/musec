#!/usr/bin/python
# -*- coding: UTF-8 -*-
from downloader import dl_album,dl_song,dl_plist
from requests.packages import urllib3
import json
import os

# Three_Party_Lib:requests,mutagen


# disable ssl warning:
urllib3.disable_warnings()

curdir = os.path.dirname(__file__)
pfile_path = '~/.config/musec/setting.json'

if os.path.exists(pfile_path):
    with open(pfile_path) as profile:
        setting = json.load(profile)
else:
    with open(os.path.join(curdir,'config/setting.json')) as profile:
        setting = json.load(profile)

path     = setting['donwload_path']
platform = setting['platform']
sformat  = setting['download_format']
info     = setting['download_info']
errcha   = setting['error_cha']

#dl_song(mid, path, platform, info, errcha, sformat)

# ct:Start to download from ct
#dl_album(mid, path, platform, info, errcha, sformat, ct=0)
#dl_plist(mid, path, platform, info, errcha, sformat, ct=0)
