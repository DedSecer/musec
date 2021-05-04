# -*- coding: UTF-8 -*-
import tools
import re
from requests import get
import os
from Musec import Musec
from html import unescape



setting = tools.load_setting()
uin = setting['uin']

path = setting['path']
sformat = setting['sformat']
info = setting['info']
uin = setting['uin']
cookies = setting['cookies']
platform = setting['platform']

def dl_song(mid, path=path, platform=platform, download_info=info, uin=uin, cookies=cookies, sformat=sformat):
    asong = Musec(mid, platform, sformat=sformat)
    scode = asong.download(path, uin=uin, cookies=cookies, download_info=download_info)
    if scode == 200:
        print(asong.name + "\ndownload successful")
    else:
        print('Fail to download %s,statu code:%d' % (asong.name, scode))

def dl_album(mid, path=path, platform=platform, download_info=info, uin=uin, cookies=cookies, sformat=sformat, ct=0):
    # ct:Start to download from ct
    aburl = 'https://y.qq.com/n/yqq/album/' + mid + '.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                      '74.0.3729.169 Safari/537.36'
        }
    h = get(aburl, headers=headers, verify=False)
    m_list= re.findall('''<a\s*href="//y.qq.com/n/yqq/song/(.*?).html"\s*title="''', h.text)

    #album_info:
    art = tools.del_cn(re.search('<a\shref=.*?data-mid=.*?title="(.*?)">', h.text, re.S).group(1))
    art = unescape(art)
    alb = re.search('''albumname : "(.*?)"''', h.text).group(1)
    alb = unescape(alb)
    imgurl = 'https:'+re.search('''<img\sid="albumImg"\s*src="(.*?)"\s*onerror''', h.text).group(1)
    imgcon = get(imgurl, headers=headers,verify=False).content

    dl_mlist(m_list,
        path,
        platform=platform,
        download_info=download_info,
        uin=uin,
        cookies=cookies,
        sformat=sformat,
        ct=ct,
        art=art,
        list_n=alb,
        imgcon=imgcon)



def dl_plist(lid, path=path, platform=platform, download_info=info, uin=uin, cookies=cookies, sformat=sformat, ct=0):
    # Download songs from QQMusic playlist
    # ct:Start to download from ct
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'dnt': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                      '76.0.3809.100 Safari/537.36',
        'sec-fetch-mod': 'cors',
        'orgin': 'https://y.qq.com',
        'sec-fetch-site': 'cors',
        'referer': 'https://y.qq.com/n/yqq/playlist/%s.html' % (lid),
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9'
    }
    url = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?type=1&json=1&utf8=1&onlysong=0&new_format=1&disstid=%s&g_tk=1647959537&loginUin=2465216809&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0' \
        % (lid)


    h = get(url, verify=False, headers=headers)
    dir = h.json()
    #songlist = []                           # list including the name of songs in the playlist
    songmid = []                            # list including the songmid of songs in the playlist
    dissname = dir['cdlist'][0]['dissname'] # name of the playlist

    for a in dir['cdlist'][0]['songlist']:
        #songlist.append(a['name'])
        songmid.append(a['mid'])

    dl_mlist(songmid,
        path,
        platform=platform,
        download_info=download_info,
        uin=uin,
        cookies=cookies,
        sformat=sformat,
        ct=ct,
        list_n=dissname)

def dl_mlist(mlist, path=path, list_n='', art='' ,imgcon='', platform=platform, download_info=info, uin=uin, cookies=cookies, sformat=sformat, ct=0):   
    # Download songs from songmid list
    # ct:Start to download from ct
    
    # Status
    total = 0
    complete = 0
    fail = 0

    errcha = tools.get_errcha(platform)
    apath = os.path.join(path, re.sub(errcha, '-', list_n))

    if not os.path.exists(apath):
    #creat the folder if do not have the mid list folder
        os.makedirs(apath)
    ln = len(mlist)

    print(list_n + '\t' + 'start to download')

    for n in list(range(ct, ln)):
        mid = mlist[n]
        asong = Musec(mid, platform=platform, art=art, img=imgcon, sformat=sformat)
        scode = asong.download(apath,
            uin=uin,
            cookies=cookies,
            download_info=download_info)

        if scode == 200:
            print('%s download successful!\t[%d/%d]' % (asong.name, n+1, ln))
            complete += 1
            total += 1
        else:
            print('[E]Fail to download %s,statu code:%d\t[%d/%d]' \
                % (asong.name, scode, n+1, ln))
            fail += 1
            total += 1

    if fail != 0:
        print('Download complete.\ttotal:%d\tcomplete:%d\tfail:%d' \
            % (ln, complete, fail))
    else:
        print('All download complete, no error output.')
