from tool import set_info
from html import unescape
from re import search,sub,compile
from requests import get
from requests.packages import urllib3

#three_party_lib:requests

#disable ssl warning:
urllib3.disable_warnings()

class Song():
    def __init__(self,url,system,art='',alb='',img='',type='mp3',):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        self.system=system
        self.type=type


        h=get(url, verify=False, headers=self.headers)

        #get_vkey:
        self.mid=search('yqq/song/(.*?).html',url).group(1)

        getvkurl='https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?&jsonpCallback=MusicJsonCallback&cid=205361747&songmid='+self.mid+'&filename=C400'+self.mid+'.m4a&guid=6612300644'
        ukurl= get(getvkurl, verify=False, headers=self.headers)
        self.vkey=search(r'"vkey":"(.*)"',ukurl.text).group(1)


        #info:
        self.name = unescape(search('''<h1 class="data__name_txt" .*?>(.*?)</h1>''', h.text).group(1))

        if not alb:
            self.alb = unescape(search('<li class="data_info__item">专辑：.*?title="(.*?)">', h.text).group(1))
        else:
            self.alb=alb

        if not img:
            imgul=search('<span class="data__cover">\s*?<img src="(.*?)"',h.text).group(1)
            self.img=get('https:'+imgul,verify=False,headers=self.headers).content
        else:
            self.img=img

        if not art:
            self.art=unescape(search('<div class="data__singer" title="(.*?)">',h.text).group(1))
        else:
            self.art=art






    def download(self,path,errstr='',by_alb=False):
        if self.type=='m4a':
            dlurl='http://dl.stream.qqmusic.qq.com/C400' + self.mid+ '.'+self.type+'?vkey=' + self.vkey+ '&guid=6612300644&uin=0&fromtag=66'
        elif self.type=='mp3':
            dlurl = 'http://dl.stream.qqmusic.qq.com/M500' + self.mid + '.' + self.type + '?vkey=' + self.vkey + '&guid=6612300644&uin=0&fromtag=55'
        h=get(dlurl,verify=False,headers=self.headers)

        if self.system=='mac':
            if not errstr:
                errstr=compile('[/]')
            song_path=path+'/'+sub(errstr,' ',self.name)+'.'+self.type
            with open(song_path,'wb') as f:
                f.write(h.content)

        elif self.system=='windows':
            if not errstr:
                errstr=compile('[<>/\\|:"*?]')
            song_path=path+'/'+sub(errstr,' ',self.name)+'.'+self.type
            with open(song_path,'wb') as f:
                f.write(h.content)

        set_info(song_path,
                 type=self.type,
                 nam=self.name,
                 art=self.art,
                 alb=self.alb,
                 img=self.img)
        if not by_alb:
            print(self.name+"\ndownload successful")



    def set_local_info(self,file):
        set_info(file,
                 nam=self.name,
                 alb=self.alb,
                 art=self.art,
                 img=self.img,
                 type=self.type)