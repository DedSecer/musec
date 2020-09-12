from argparse import ArgumentParser as Argparser
from downloader import dl_album,dl_song,dl_plist
from requests.packages import urllib3

#disable ssl warning:
urllib3.disable_warnings()


parser = Argparser()

parser.add_argument('typ',action="store")
parser.add_argument('-u',action="store",dest='url')
parser.add_argument('-p',action="store",dest='path')
parser.add_argument('-s',action="store",dest='platform')

arg=parser.parse_args()


if arg.typ == 'music':
    dl_song(arg.url,arg.path,arg.platform,type)

