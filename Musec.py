# -*- coding: UTF-8 -*-
import tools
from html import unescape
from bs4 import BeautifulSoup as BS
import re
from requests import get
import os

class Musec():
    def __init__(self, mid, platform, albn='', art='', img='', sformat='m4a'):
        self.guid = '8962339369'
        self.mid = mid

        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        self.platform = platform
        self.sformat = sformat

        #Info
        h=get('http://y.qq.com/n/ryqq/songDetail/%s' % (mid), verify=False, headers=self.headers)
        soup = BS(h.text, 'html.parser')

        self.name = unescape(soup.select('div.data__name > h1')[0].string)

        if albn:
            self.albn = albn
        else:
            try:
                self.albn = unescape(soup.select('li.data_info__item_song > a')[0].string)
            except IndexError: # Song has no album
                self.albn = ' '

        if img:
            self.img = img
        else:
            part = '.*?window.__INITIAL_DATA__ ={"detail":{"title":"%s","picurl":"(.*?)"' % (re.escape(self.name).replace('"', '\\\\"').replace('/','\\\\u002F'))
            #part = '.*?window.__INITIAL_DATA__ ={"detail":{"title":"%s","picurl":"(.*?)"' % (self.name.replace('"', '\\\\"').replace('/','\\\\u002F').replace('(', '\\(').replace(')', '\\)'))
            scripts = set(soup.select('script')) - set(soup.select('script[crossorigin=anonymous]'))
            for script in scripts:
                imgurl = ''
                try:
                    imgurl = 'http:' + re.match(part, script.text).group(1).replace('\\u002F', '/')
                    break
                except AttributeError:
                    pass
            self.img = get(imgurl, verify=False, headers=self.headers).content

        if art:
            self.art = art
        else:
            art = ''
            for s in soup.select('a.data__singer_txt'):
                art += s.string + ' / '
            self.art = tools.del_cn(unescape(art[:-3]))

    def get_download_url(self, uin='0', cookies={}):
        #get_vkey:
        getvkurl = 'http://u.y.qq.com/cgi-bin/musicu.fcg?&data={"req":{"param":{"guid":"%s"}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"%s","songmid":["%s"],"uin":"%s"}},"comm":{"uin":%s}}' \
                    % (self.guid, self.guid, self.mid, uin, uin)

        vkres = get(getvkurl, verify=False, headers=self.headers, cookies=cookies)
        purl = vkres.json()['req_0']['data']['midurlinfo'][0]['purl']

        self.dlurl = 'http://dl.stream.qqmusic.qq.com/' + purl




    def download(self, path, uin='0', cookies={}, download_info=True):
        self.get_download_url(uin, cookies)
        h = get(self.dlurl, cookies=cookies, verify=False, headers=self.headers)

        if h.status_code == 200:
            # filter error character
            errcha = tools.get_errcha(self.platform)
            filename = re.sub(errcha, '-' , self.name) + '.' + self.sformat
            song_path = os.path.join(path, filename)

            with open(song_path, 'wb') as f:
                f.write(h.content)

            if download_info:
                tools.set_info(
                    song_path,
                    sformat=self.sformat,
                    nam=self.name,
                    art=self.art,
                    alb=self.albn,
                    img=self.img)
        return h.status_code
