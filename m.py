from downloader import dl_album,dl_song,dl_plist
from requests.packages import urllib3

#Three_Party_Lib:requests,mutagen


#disable ssl warning:
urllib3.disable_warnings()

#type:mp3,m4a

#dl_song(url,path,system,type='mp3')
#dl_album(mid='000SBmte03ICax',path='/Users/kenan/Desktop/1',system='mac',type='mp3',ct=0)   #ct:Start to download from ct
dl_plist('4203712973','/Users/kenan/Desktop/1',system='mac',type='m4a',ct=30)#a function to download songs from QQMusic playlist

