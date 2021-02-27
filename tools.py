# -*- coding: UTF-8 -*-
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
from mutagen.mp4 import MP4Cover
from mutagen import File
from re import search,compile

import platform as pf
import json
import os
import shutil


def set_info(file, sformat, art='', alb='', img='', nam=''):
    if sformat == 'm4a':
        mu = File(file)
        if art:
            mu['©ART'] = art
        if alb:
            mu['©alb'] = alb
        if img:
            mu['covr'] = [MP4Cover(img)]
        if nam:
            mu['©nam'] = nam
        mu.save()
    elif sformat=='mp3':
        audio = ID3(file)
        if img:
            #img:
            audio['APIC'] = APIC(encoding=3, mime='image/jpeg', sformat=3, desc=u'Cover', data=img)
        if nam:
            #title
            audio['TIT2'] = TIT2(encoding=3, text=[nam])
        if art:
            #art:
            audio['TPE1'] = TPE1(encoding=3, text=[art])
        if alb:
            #album:
            audio['TALB'] = TALB(encoding=3, text=[alb])
        audio.save()



def del_cn(str):
    try:
        p = search('(\(.*?\))',str).group(1)
    except AttributeError:
        pass
    else:
        if p:
            str = str.replace(p,'')
    return str

def get_errcha(platform):#get different error character in different system platform
    if platform == 'Linux' or platform == 'Darwin':
        errcha = compile('[/]')

    elif platform == 'Windows':
        errcha = compile('[<>/\\|:"*?]')
    else:
        print('Please input currect system platform')
        exit(1)
    return errcha

def load_setting():
        
    if pf.system() == 'Linux' or pf.system() == 'Darwin':
        pfile_path = os.path.join(os.environ['HOME'],'.config/musec/setting.json')
    elif pf.system() == 'Windows':
        pfile_path = os.path.join(os.environ['APPDATA'],'musec\\setting.json')


    if not os.path.exists(pfile_path):
        if not os.path.exists(os.path.split(pfile_path)[0]):
            os.makedirs(os.path.split(pfile_path)[0])
        shutil.copyfile('config/setting.json',pfile_path)

    with open(pfile_path) as profile:
        setting = json.load(profile)


    path     = setting['donwload_path']
    sformat  = setting['download_format']
    info     = setting['download_info']
    errcha   = setting['error_cha']
    uin      = setting['uin']

    platform = setting['platform']
    if platform == 'Auto':
        platform = pf.system()


    # cookies
    cookies = ''

    # load cookies from strings like this: 'aaa=bbb; ccc=ddd....'
    cookies_str = ''
    if cookies_str:
        cookies = {}
        for line in cookies_str.split(';'):
            name,value=line.strip().split('=',1)
            cookies[name]=value  

    # load cookies if exist cookies.json
    elif os.path.exists('config/cookies.json'):
        with open('config/cookies.json') as f:
            cookies = json.load(f)
    return {
        'path': path,
        'sformat': sformat,
        'info': info,
        'errcha': errcha,
        'uin': uin,
        'platform': platform,
        'cookies': cookies
    }