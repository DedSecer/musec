from downloader import dl_album,dl_song
from requests.packages import urllib3

#Three_Party_Lib:requests,mutagen


#disable ssl warning:
urllib3.disable_warnings()

#dl_song(url,path,system,type='mp3')
#dl_album(mid,path,system,type='mp3',ct=0)   ct:Start to download from ct

