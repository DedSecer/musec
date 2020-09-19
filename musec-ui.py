from downloader import dl_album,dl_song,dl_plist
from requests.packages import urllib3
import json
import os
from shutil import copy as shutil_copy


#disable ssl warning:
urllib3.disable_warnings()


try: # unix
    home_path=os.environ['HOME']
except KeyError: # windows
    home_path=os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'])

pfile_path = os.path.join(home_path, '.config/musec/setting.json')

if os.path.exists(pfile_path):
    pass
else:
    try:
        os.mkdir(os.path.join(home_path, '.config/musec'))
    except:
        pass
    shutil_copy('./config/setting.json',pfile_path)

with open(pfile_path) as profile:
    setting = json.load(profile)

errcha = setting['error_cha']

method = input('All donwload method:\n1) single\t2) album\t3) playlist\nChoose a method (default=1): ')
mid = input('Mid: ')
path = input('Donwload path (default read from setting): ')
platform = input('1) unix\t2)windows\n Choose system platform (default read from setting): ')
info = input('1) donwload song info\t2)do not download song info\nEnter a selection (default=1): ')
sformat = input('1)m4a\n Choose song format (default=1):')

# set default
if not method:
    method = '1'
if not path:
    path = setting['donwload_path']

if not platform:
    platform = setting['platform']
elif platform =='1':
    platform = 'unix'
elif platform =='2':
    platform = 'windows'

if not info:
    info = setting['download_info']
elif info == '1':
    info = True
elif info == '2':
    info = False

if not sformat:
    sformat = setting['download_format']
elif sformat == '1':
    sformat = 'm4a'


if method == '1':
    dl_song(mid, path, platform, info, errcha, sformat)

elif method > '1':
    ct = input('index of song to download within list: ')
    if not ct:
        ct = 0
    else:
        ct = int(ct)
    if method == '2':
        dl_album(mid, path, platform, info, errcha, sformat, ct)
    elif method == '3':
        dl_plist(mid, path, platform, info, errcha, sformat, ct)
