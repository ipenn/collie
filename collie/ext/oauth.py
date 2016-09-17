# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/8 0008.
from flask_oauthlib.provider import OAuth2Provider
from flask_oauthlib.client import OAuth
from collie.modules.accounts.models import User, Client, Grant, Token
from datetime import datetime, timedelta
from flask import render_template, request, \
    make_response, jsonify, session, redirect, url_for


def create_provider(app):
    oauth = OAuth2Provider(app)

    @oauth.clientgetter
    def get_client(client_id):
        return Client.objects(client_id=client_id).first()

    @oauth.grantgetter
    def get_grant(client_id, code):
        return Grant.objects(client_id=client_id, code=code).first()

    @oauth.tokengetter
    def get_token(access_token=None, refresh_token=None):
        if access_token:
            return Token.objects(access_token=access_token).first()
        if refresh_token:
            return Token.objects(refresh_token=refresh_token).first()
        return None

    @oauth.grantsetter
    def set_grant(client_id, code, request, *args, **kwargs):
        expires = datetime.utcnow() + timedelta(seconds=100)
        grant = Grant(
            client_id=client_id,
            code=code['code'],
            redirect_uri=request.redirect_uri,
            scopes=request.scopes,
            expires=expires,
        )
        grant.save()

    @oauth.tokensetter
    def set_token(token, request, *args, **kwargs):
        test = token
        print()
        tok = Token(
            access_token=token.get('access_token'),
            refresh_token=token.get('refresh_token'),
            client_id=request.client.client_id,
            scopes=token.scopes,
            expires=datetime.utcnow() + timedelta(seconds=token.get('expires_in'))
        )
        tok.save()

    @oauth.usergetter
    def get_user(username, password, *args, **kwargs):
        return User.objects.filter_by(username=username).first()

    return oauth


def prepare_app():
    client1 = Client(
        name='dev', client_id='dev', client_secret='dev',
        redirect_uris=['http://local.wushuyi.com:8000/authorized',
                       'http://local.wushuyi.com:8000/',
                       'http://local.wushuyi.com:5000/authorized',
                       'http://local.wushuyi.com/authorized']
    )

    client2 = Client(
        name='confidential', client_id='confidential',
        client_secret='confidential', client_type='confidential',
        redirect_uris=['http://local.wushuyi.com:8000/authorized',
                       'http://local.wushuyi.com:8000/',
                       'http://local.wushuyi.com:5000/authorized',
                       'http://local.wushuyi.com/authorized']
    )
    temp_grant = Grant(
        client_id='confidential',
        code='12345', scopes=['email'],
        expires=datetime.utcnow() + timedelta(seconds=100)
    )
    access_token = Token(
        client_id='dev',
        access_token='expired',
        expires=datetime.utcnow() + timedelta(seconds=0)
    )

    client1.save()
    client2.save()
    temp_grant.save()
    access_token.save()


def create_server(app, oauth=None):
    if not oauth:
        oauth = create_provider(app)

    if not Client.objects.count():
        prepare_app()

    @app.route('/home')
    def home():
        return render_template('home.html')

    @app.route('/oauth/authorize', methods=['GET', 'POST'])
    @oauth.authorize_handler
    def authorize(*args, **kwargs):
        # NOTICE: for real project, you need to require login
        if request.method == 'GET':
            # render a page for user to confirm the authorization
            # return True
            return render_template('confirm.html')

        if request.method == 'HEAD':
            # if HEAD is supported properly, request parameters like
            # client_id should be validated the same way as for 'GET'
            response = make_response('', 200)
            response.headers['X-Client-ID'] = kwargs.get('client_id')
            return response

        confirm = request.form.get('confirm', 'no')
        return confirm == 'yes'

    @app.route('/oauth/errors')
    def showerror():
        return request.args.get('error')

    @app.route('/oauth/token', methods=['POST', 'GET'])
    @oauth.token_handler
    def access_token():
        return {}

    @app.route('/oauth/revoke', methods=['POST'])
    @oauth.revoke_handler
    def revoke_token():
        pass

    @app.route('/api/email')
    @oauth.require_oauth('email')
    def email_api():
        return jsonify(email='me@oauth.net', username='wushuyi')


def create_client(app):
    oauth = OAuth(app)

    remote = oauth.remote_app(
        'dev',
        consumer_key='dev',
        consumer_secret='dev',
        request_token_params={'scope': 'address email'},
        base_url='http://local.wushuyi.com:5000/api/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='http://local.wushuyi.com:5000/oauth/token',
        authorize_url='http://local.wushuyi.com:5000/oauth/authorize'
    )

    # @app.route('/')
    # def index():
    #     if 'dev_token' in session:
    #         print(session.get('dev_token'))
    #         ret = remote.get('email')
    #         return jsonify(ret.data)
    #     return redirect(url_for('login'))

    @app.route('/login')
    def login():
        return remote.authorize(callback=url_for('authorized', _external=True))

    @app.route('/logout')
    def logout():
        session.pop('dev_token', None)
        return redirect(url_for('index'))

    @app.route('/authorized')
    def authorized():
        # res = request.args.get('code')
        # return res
        resp = remote.authorized_response()
        if resp is None:
            return 'Access denied: error=%s' % (
                request.args['error']
            )
        if isinstance(resp, dict) and 'access_token' in resp:
            session['dev_token'] = (resp['access_token'], '')
            return jsonify(resp)
        return str(resp)

    @remote.tokengetter
    def get_oauth_token():
        return session.get('dev_token')

    return remote
