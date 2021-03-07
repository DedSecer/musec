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
uin = setting['uin']
cookies = setting['cookies']
platform = setting['platform']



#dl_song(mid, path=path, platform=platform, download_info=info, uin=uin, cookies=cookies, sformat=sformat, ct=0)
#dl_album(mid, path=path, platform=platform, download_info=info, uin=uin, cookies=cookies, sformat=sformat, ct=0)
#dl_plist(mid, path=path, platform=platform, download_info=info, uin=uin, cookies=cookies, sformat=sformat, ct=0)
