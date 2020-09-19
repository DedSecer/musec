from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
from mutagen.mp4 import MP4Cover
from mutagen import File
from re import search,compile

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
    if platform == 'unix':
        errcha = compile('[/]')

    elif platform == 'windows':
        errcha = compile('[<>/\\|:"*?]')
    else:
        print('Please input currect system platform')
        exit(1)
    return errcha
