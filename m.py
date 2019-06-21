import requests
import re
import os
from requests.packages import urllib3
from mutagen.mp4 import MP4Cover
import mutagen
from html import unescape

urllib3.disable_warnings()


class Song():
    def __init__(self,url,system,art='',alb='',img=''):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        self.system=system

        h=requests.get(url, verify=False, headers=self.headers)

        #get_vkey:
        self.mid=re.search('yqq/song/(.*?).html',url).group(1)

        getvkurl='https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?&jsonpCallback=MusicJsonCallback&cid=205361747&songmid='+self.mid+'&filename=C400'+self.mid+'.m4a&guid=6612300644'
        ukurl= requests.get(getvkurl, verify=False, headers=self.headers)
        self.vkey=re.search(r'"vkey":"(.*)"',ukurl.text).group(1)


        #info:
        self.name = unescape(re.search('''<h1 class="data__name_txt" .*?>(.*?)</h1>''', h.text).group(1))

        if not alb:
            self.alb = unescape(re.search('<li class="data_info__item">专辑：.*?title="(.*?)">', h.text).group(1))
        else:
            self.alb=alb

        if not img:
            imgul=re.search('<span class="data__cover">\s*?<img src="(.*?)"',h.text).group(1)
            self.img=requests.get('https:'+imgul,verify=False,headers=self.headers).content
        else:
            self.img=img

        if not art:
            self.art=unescape(re.search('<div class="data__singer" title="(.*?)">',h.text).group(1))
        else:
            self.art=art






    def download(self,path,errstr=''):
        dlurl='http://dl.stream.qqmusic.qq.com/C400' + self.mid+ '.m4a?vkey=' + self.vkey+ '&guid=6612300644&uin=0&fromtag=66'

        h=requests.get(dlurl,verify=False,headers=self.headers)

        if self.system=='mac':
            song_path=path+'/'+self.name+'.m4a'
            with open(song_path,'wb') as f:
                f.write(h.content)

        elif self.system=='windows':
            if not errstr:
                errstr=errstr=re.compile('[<>/\\|:"*?]')
            song_path=path+'/'+re.sub(errstr,' ',self.name)+'.m4a'
            with open(song_path,'wb') as f:
                f.write(h.content)

        set_info(song_path,
                 nam=self.name,
                 art=self.art,
                 alb=self.alb,
                 img=self.img)


            
        


def dl_album(mid,path,system,ct=0):
    aburl='https://y.qq.com/n/yqq/album/'+mid+'.html'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    h=requests.get(aburl,headers=headers,verify=False)
    m_list=re.findall('''<a\s*href="//y.qq.com/n/yqq/song/(.*?).html"\s*title="''',h.text)

    #album_info:
    art=del_cn(re.search('<a\shref=.*?data-mid=.*?title="(.*?)">',h.text,re.S).group(1))
    alb=re.search('''"albumname":"(.*?)"''',h.text).group(1)
    imgurl = 'https:'+re.search('''<img\sid="albumImg"\s*src="(.*?)"\s*onerror''', h.text).group(1)
    imgcon=requests.get(imgurl,headers=headers,verify=False).content

    if system=='mac':
        apath=path+'/'+alb
        errstr=''
    elif system=='windows':
        errstr=re.compile('[<>/\\|:"*?]')
        apath=path+'\\'+re.sub(errstr,'',alb)


    # start_to_download:
    if ct==0 and not os.path.exists(apath):
        os.makedirs(apath)

    ln=len(m_list)
    print(alb+'\tstart to download')
    for n in list(range(ct,ln)):
        m=m_list[n]
        url='https://y.qq.com/n/yqq/song/'+m+'.html'
        asong=Song(url,art=art,alb=alb,img=imgcon,system=system)
        asong.download(apath,errstr)
        print(asong.name,'\tdownload successful!\t[',n+1,'/',ln,']')



def set_info(file,art='',alb='',img='',nam=''):
    mu=mutagen.File(file)
    if art:
        mu['©ART']=art
    if alb:
        mu['©alb']=alb
    if img:
        mu['covr']=[MP4Cover(img)]
    if nam:
        mu['©nam']=nam
    mu.save()

def del_cn(str):
    p=re.search('(\(.*?\))',str).group(1)
    if p:
        str=str.replace(p,'')
    return str







def error(msg):
    print(msg+' error')
    a=input('按enter（return）键退出')
    exit()
def run():
    print('注意：仅能下载qq音乐免费播放的歌曲\n如果有问题，请联系：\n2465216809（qq微信同号）' )
    v=input('按enter(return)键继续')
    while True:
        print('请选择：')

        sb=input('1.单曲下载； 2.专辑下载；3.退出')
        try:
            sb=int(sb)
        except:
            error('input')

        if sb==1:
            url=input('请输入下载歌曲详细界面的url')

            try:
                song=Song(url)
            except:
                error('url')
            else:
                path=input('请输入下载地址')
                try:
                    song.download(path)
                except:
                    error('path')
                print(song.name+'\tdownload successful')

        elif sb==2:
            mid=input('请输入专辑mid（就是网址中album／到.html中的一段数字加字母）')
            path=input('请输入下载位置')
            print('将在下载位置中创间一个名为专辑名字的文件夹')
            try:
                dl_album(mid,path)
            except:
                error('album')
        elif sb==3:
            break



