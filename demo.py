from downloader import dl_album,dl_song,dl_plist
from requests.packages import urllib3

#Three_Party_Lib:requests,mutagen


#disable ssl warning:
urllib3.disable_warnings()

#type:mp3,m4a

#dl_song(url,path,system,type)
#dl_album(mid,path,system,type,ct=0)   #ct:Start to download from ct
#dl_plist(url,path,system,type,ct=0)#a function to download songs from QQMusic playlist

