import os
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    Response,
    make_response
)
from urllib.parse import parse_qs, urljoin, urlencode
from auth import District833User
from cache import UserCache
from db import DB
from util import make_cookie


app = Flask(__name__)
cookie_name = os.getenv('COOKIE_NAME')


@app.route('/')
def index():
    if cookie := request.cookies.get(cookie_name, None):
        if token := DB.get_token(cookie):
            if (user := UserCache.get(token)) is None:
                user = DB.get_user(token)
            if user is not None:
                return render_template('profile.html', me=user.sc.get_me())
    resp = make_response(render_template('index.html'))
    resp.set_cookie(cookie_name, make_cookie())
    return resp


@app.route('/login')
def login():
    if token := request.args.get('oauth_token'):
        if user := UserCache.get(token):
            if user.validate_auth():
                if cookie := request.cookies.get(cookie_name):
                    DB.save_token(cookie, token)
                return redirect('/')
            return render_template('login.html', message='Login failed')
        return Response('User not recognized', 404)
    return render_template('login.html')
    

@app.route('/auth/login')
def auth():
    user = District833User()
    UserCache.add(user)
    url = user.request_url(urljoin(
        request.host_url,
        '/login'
    ))
    return redirect(url)


if __name__ == '__main__':
    app.run(
        '0.0.0.0',
        8080
    )
