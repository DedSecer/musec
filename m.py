from downloader import dl_album,dl_song
from requests.packages import urllib3

#Three_Party_Lib:requests,mutagen


#disable ssl warning:
urllib3.disable_warnings()

dl_song('https://y.qq.com/n/yqq/song/003pp8Ns3fyc22.html','/Users/kenan/Desktop/de',system='mac',type='mp3')  #type:mp3,m4a
#dl_album(mid,path,system,type='mp3',ct=0)   #ct:Start to download from ct

