from tool import del_cn,get_errcha
import re
from requests import get
import os
from Song import Song
from requests.packages import urllib3
from html import unescape

#three_party_lib:requests

#disable ssl warning:
urllib3.disable_warnings()


def dl_song(url, path, system, type='mp3'):
    asong = Song(url,system,type=type)
    asong.download(path)


def dl_mlist(mlist, path, system, way, type='mp3', ct=0, art='', list_n='', imgcon=''):   
    # Download songs from songmid list
    if system == 'unix':
        errcha = re.compile('[/]')
        apath = path + '/' + re.sub(errcha, ' ', list_n)

    elif system == 'windows':
        errcha = re.compile('[<>/\\|:"*?]')
        apath = path + '\\' + re.sub(errcha, ' ', list_n)
    else:
        print('Please input currect system')
        exit(1)

    if ct == 0 and not os.path.exists(apath):#creat the folder if do not have the mid list folder,
        os.makedirs(apath)
    ln = len(mlist)
    errcha = get_errcha(system)

    print(list_n + '\t' + 'start to download')

    for n in list(range(ct, ln)):
        mid = mlist[n]
        url = 'https://y.qq.com/n/yqq/song/' + mid + '.html'

        if way == 'alb':
            asong = Song(url, art=art, alb=list_n, img=imgcon, system=system, type=type)
            asong.download(apath, errcha, originality=False)

        else:
            asong = Song(url,system=system,type=type)
            asong.download(apath, errcha, originality=False)

        print(asong.name, '\tdownload successful!\t[', n + 1, '/', ln, ']')


def dl_album(mid, path, system, type='mp3', ct=0):#  ct:Start to download from ct
    aburl = 'https://y.qq.com/n/yqq/album/' + mid + '.html'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    h = get(aburl, headers=headers, verify=False)
    m_list= re.findall('''<a\s*href="//y.qq.com/n/yqq/song/(.*?).html"\s*title="''', h.text)

    #album_info:
    art = del_cn(re.search('<a\shref=.*?data-mid=.*?title="(.*?)">',h.text,re.S).group(1))
    art = unescape(art)
    alb = re.search('''albumname : "(.*?)"''', h.text).group(1)
    alb = unescape(alb)
    imgurl = 'https:'+re.search('''<img\sid="albumImg"\s*src="(.*?)"\s*onerror''', h.text).group(1)
    imgcon = get(imgurl, headers=headers,verify=False).content

    dl_mlist(m_list, path, system, 'alb', type=type, ct=ct, art=art, list_n=alb, imgcon=imgcon)



def dl_plist(lid, path, system, type='mp3', ct=0):
    #Download songs from QQMusic playlist
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'dnt': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                      '76.0.3809.100 Safari/537.36',
        'sec-fetch-mod': 'cors',
        'orgin': 'https://y.qq.com',
        'sec-fetch-site': 'cors',
        'referer': 'https://y.qq.com/n/yqq/playlist/'+lid+'.html',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9'
    }
    url = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?type=1&json=1&utf8=1&onlysong=0&new_format=1&' \
          'disstid='+lid+'&g_tk=1647959537&loginUin=2465216809&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&' \
          'notice=0&platform=yqq.json&needNewCode=0'


    h = get(url, verify=False, headers=headers)
    dir = h.json()
    songlist = []                           # list including the name of songs in the playlist
    songmid = []                            # list inclouding the songmid of songs in the playlist
    dissname = dir['cdlist'][0]['dissname'] #name of the playlist

    for a in dir['cdlist'][0]['songlist']:
        songlist.append(a['name'])
        songmid.append(a['mid'])
    dl_mlist(songmid, path, system=system, way='plist', type=type, ct=ct, list_n=dissname)
