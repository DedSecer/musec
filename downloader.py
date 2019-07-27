from tool import del_cn
import re
from requests import get
import os
from Song import Song
from requests.packages import urllib3

#three_party_lib:requests

#disable ssl warning:
urllib3.disable_warnings()


def dl_song(url,path,system,type='mp3'):
    asong=Song(url,system,type=type)
    asong.download(path)




def dl_album(mid,path,system,type='mp3',ct=0):#  ct:Start to download from ct
    aburl='https://y.qq.com/n/yqq/album/'+mid+'.html'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    h=get(aburl,headers=headers,verify=False)
    m_list=re.findall('''<a\s*href="//y.qq.com/n/yqq/song/(.*?).html"\s*title="''',h.text)

    #album_info:
    art=del_cn(re.search('<a\shref=.*?data-mid=.*?title="(.*?)">',h.text,re.S).group(1))
    alb=re.search('''"albumname":"(.*?)"''',h.text).group(1)
    imgurl = 'https:'+re.search('''<img\sid="albumImg"\s*src="(.*?)"\s*onerror''', h.text).group(1)
    imgcon=get(imgurl,headers=headers,verify=False).content

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

