import requests
import json
from pprint import pprint


def search_song(key, pageNo='1', pageSize='20'):
    url = 'https://c.y.qq.com/soso/fcgi-bin/search_for_qq_cp'
    headers = {
        'Referer': 'https://y.qq.com'
    }
 
    params = {
        'format': 'json',
        'n': pageSize,
        'p': pageNo,
        'w': key,
        'cr': '1',
        'g_tk': '5381',
        't': '0',
    }

    res=requests.get(url,headers=headers,params=params)
    song_list=json.loads(res.text)['data']['song']['list']
    return song_list