# -*- coding: UTF-8 -*-
from downloader import dl_album, dl_song, dl_plist
from requests.packages import urllib3
from tools import load_setting

# disable ssl warning:
urllib3.disable_warnings()

setting = load_setting()
path = setting['path']
sformat = setting['sformat']
info = setting['info']
errcha = setting['errcha']
uin = setting['uin']
cookies = setting['cookies']
platform = setting['platform']



#dl_song(mid, path, platform, info, uin, cookies, errcha, sformat)
#dl_album(mid, ct=0, path, platform, info, uin, cookies, errcha, sformat)
#dl_plist(mid, ct=0, path, platform, info, uin, cookies, errcha, sformat)
