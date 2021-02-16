from flask import Flask
import flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Welcome to My Watchlist!'

@app.route('/search/')
def search_page():
    search_text = flask.request.args.get('q')
    if search_text:
        return search_text
    else:
        return flask.render_template('search_page.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')