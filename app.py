from flask import Flask
import flask

import searcher

from Musec import Musec


app = Flask(__name__,template_folder='flask_app/templates',static_folder='flask_app/static')

@app.route('/')
def hello():
    return 'Welcome!'

@app.route('/search/')
def search_page():
    search_text = flask.request.args.get('q')
    if search_text:
        # return str(searcher.search_song(search_text))
        return flask.render_template('result.html',datas=searcher.search_song(search_text))

    else:
        return flask.render_template('search_page.html')

    
@app.route('/download/<mid>')
def download(mid):
    platform = 'Linux'
    tmp_dir = '/tmp'


    asong = Musec(mid, platform=platform)
    asong.download(path=tmp_dir)
    return flask.send_from_directory(tmp_dir, asong.filename)
    # return mid


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)
