import tools
from html import unescape
import re
from requests import get
import os

class Musec():
    def __init__(self, mid, platform, albn='', art='', img='', sformat='m4a'):
        self.guid = '8962339369'
        self.uin = 0
        self.mid = mid

        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        self.platform = platform
        self.sformat = sformat

        #Info
        h=get('https://y.qq.com/n/yqq/song/%s.html' % (mid), verify=False, headers=self.headers)
        self.name = unescape(re.search('''<h1 class="data__name_txt" .*?>(.*?)</h1>''', h.text).group(1))

        if albn:
            self.albn = albn
        else:
            try:
                self.albn = unescape(re.search('<li class="data_info__item">专辑：.*?title="(.*?)">', h.text).group(1))
            except AttributeError: # Song has no album
                self.albn = ' '

        if img:
            self.img = img
        else:
            imgul = re.search('<span class="data__cover">\s*?<img src="(.*?)"', h.text).group(1)
            self.img = get('https:'+imgul, verify=False, headers=self.headers).content

        if art:
            self.art = art
        else:
            self.art = unescape(re.search('<div class="data__singer" title="(.*?)">',h.text).group(1))

    def download(self, path, errcha='', download_info=True, originality=True):
        #get_vkey:
        getvkurl = 'https://u.y.qq.com/cgi-bin/musicu.fcg?&data={"req":{"param":{"guid":" %s"}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"%s","songmid":["%s"],"uin":"%s"}},"comm":{"uin":%s}}' % (self.guid, self.guid, self.mid, self.uin, self.uin)
        vkres = get(getvkurl, verify=False, headers=self.headers)
        purl = vkres.json()['req_0']['data']['midurlinfo'][0]['purl']
        dlurl = 'http://dl.stream.qqmusic.qq.com/' + purl

        h = get(dlurl, verify=False, headers=self.headers)

        if h.status_code == 200:
            # filter error character
            if not errcha:
                errcha = tools.get_errcha(self.platform)
            filename = re.sub(errcha, '-' , self.name) + '.' + self.sformat
            song_path = os.path.join(path, filename)

            with open(song_path, 'wb') as f:
                f.write(h.content)

            if download_info:
                tools.set_info(song_path, sformat=self.sformat, nam=self.name, art=self.art, alb=self.albn, img=self.img)
            if originality:
                print(self.name + "\ndownload successful")
        else:
            if originality:
                print('Fail to download %s,statu code:%d' % (self.name, h.status_code))
        return h.status_code
