# MUSEC
基于python requests的QQ音乐API，主要用于下载音乐，并且通过`mutagen`设置音乐信息。

### requriments：
* python3.x
* requests、mutagen、beautifulsoup4(python第三方库)

#### Tips:此项目仅供学习和参考。

## Quick Start
首次运行demo.py会将`setting.json`复制到本地（linux或macOS位于`$HOME/.config/musec/setting.json`,windows位于`%APPDATA%\musec\setting.json`）可以根据情况编辑`setting.json`。

编辑好`setting.json`后在`demo.py`中取消注释相应的函数并修改函数中的参数。

* 注意：此项目并不能获取到所有音乐的链接，只能获取到传递的cookies所对应的账号有权播放的音乐（即vip用户可听的歌曲只有vip用户才能下载），如未传入cookies则只能获取非vip用户可播放的歌曲

### 歌曲下载
在`demo.py`中取消注释`dl_song(mid...`一行，其中mid为必选参数，如未修改其他参数则会根据`setting.json`中的设置传参。

*mid*为QQ音乐歌曲详细信息页面URL中的一串标识符，如*晴天*的详细信息页面为`https://y.qq.com/n/yqq/song/0039MnYb0qxYhV.html`,则`mid`为`0039MnYb0qxYhV`。

### 专辑下载

在`demo.py`中取消注释`dl_album(mid...`一行，参数的使用同`dl_song()`，*mid*为专辑详细信息URL中的标识符，此外参数*ct*表示从第*ct*首歌下载（顺序依据QQ音乐中的排列）.

### 歌单下载

在`demo.py`中取消注释`dl_plist(mid...`一行，参数的使用同`dl_album()`，*mid*为播放列表页面URL中的标识符。


### 在python交互式环境中运行
运行前确保在本项目`musec`目录下
```shell
$ python
>>> import downloader
>>> downloader.dl_song(mid) # 下载单曲
>>> downloader.dl_album(mid) # 下载专辑
>>> downloader.dl_plist(mid) # 下载歌单
```

### 更多函数信息和`setting.json`的说明请见[wiki](https://github.com/DedSecer/musec/wiki)界面。

## 关于cookies
可以以*JSON*的形式将*cookies*保存在`$HOME/.config/musec/cookies.josn`(windows位于`%APPDATA%\musec\cookies.json`)，或将*cookies*以*string*的形式保存在`setting.json`中的`cookies_str`项中。（`cookies.json`的优先级会高于`setting.json`中的`cookies_str`)

调用函数`dl_song()`、`dl_album()`或`dl_plist()`时会自动读取cookies。

**注意**：请务必将`uin`设置为cookies所对应的QQ账号，否则会无效。

## TODO
- [ ] 高品质音乐下载
- [ ] lrc歌词文件下载

## THE END
此项目处于开发中，仍须不断完善，如有问题或更好的想法欢迎Issues或PR。


