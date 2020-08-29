from tool import set_info
from html import unescape
from re import search,sub,compile
from requests import get
from requests.packages import urllib3

#three_party_lib:requests

#disable ssl warning:
urllib3.disable_warnings()

class Song():
    def __init__(self, uri, system, art='', alb='', img='', type='mp3'):
        if uri.startswith('http'):
            self.url = uri
        else:
            self.url = ''
        self.mid = search('yqq/song/(.*?).html', self.url).group(1)
        self.guid = '8962339369'
        self.uin = 0

        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        self.system = system
        self.type = type


        h=get(self.url, verify=False, headers=self.headers)

        #get_vkey:
        getvkurl = 'https://u.y.qq.com/cgi-bin/musicu.fcg?&data={"req":{"param":{"guid":" %s"}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"%s","songmid":["%s"],"uin":"%s"}},"comm":{"uin":%s}}'%(self.guid,self.guid,self.mid,self.uin,self.uin)

        vkres = get(getvkurl, verify=False, headers=self.headers)
        purl = vkres.json()['req_0']['data']['midurlinfo'][0]['purl']
        self.url = 'http://dl.stream.qqmusic.qq.com/' + purl

        #info:
        self.name = unescape(search('''<h1 class="data__name_txt" .*?>(.*?)</h1>''', h.text).group(1))

        if not alb:
            try:
                self.alb = unescape(search('<li class="data_info__item">专辑：.*?title="(.*?)">', h.text).group(1))
            except AttributeError: # Song has no album
                self.alb = ' '
        else:
            self.alb = alb

        if not img:
            imgul = search('<span class="data__cover">\s*?<img src="(.*?)"', h.text).group(1)
            self.img = get('https:'+imgul, verify=False, headers=self.headers).content
        else:
            self.img = img

        if not art:
            self.art = unescape(search('<div class="data__singer" title="(.*?)">',h.text).group(1))
        else:
            self.art = art






    def download(self, path, errcha='', originality=True):
        h=get(self.url, verify=False, headers=self.headers)
        
        if self.system == 'unix':
            if not errcha:
                errcha = compile('[/]')
            song_path=path + '/' + sub(errcha,' ', self.name) + '.' + self.type
            with open(song_path, 'wb') as f:
                f.write(h.content)

        elif self.system == 'windows':
            if not errcha:
                errcha = compile('[<>/\\|:"*?]')
            song_path = path + '/'+ sub(errcha,' ', self.name) + '.' + self.type
            with open(song_path, 'wb') as f:
                f.write(h.content)
        else:
            print('Please input currect system')
            exit(1)

        set_info(song_path,
                 type=self.type,
                 nam=self.name,
                 art=self.art,
                 alb=self.alb,
                 img=self.img)
        if originality:
            print(self.name + "\ndownload successful")



    def set_local_info(self, file):
        set_info(file,
                 nam=self.name,
                 alb=self.alb,
                 art=self.art,
                 img=self.img,
                 type=self.type)
