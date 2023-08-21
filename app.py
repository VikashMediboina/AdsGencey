from flask import Flask, redirect, url_for, session, render_template
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = 'your_secret_key'

oauth = OAuth(app)

github = oauth.remote_app(
    'github',
    consumer_key='c65c3a1e3a792b5da88f',
    consumer_secret='492a8137ca5fa31a8207909fcee9b8f1c71ae5c8',
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'github_token' in session:
        user_data = github.get('user').data
        return render_template('dashboard.html', username=user_data['login'],public_repos=user_data['public_repos'],followers=user_data['followers'],following=user_data['following'])
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return github.authorize(callback=url_for('github_authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('github_token', None)
    return render_template('login.html')


@app.route('/login/authorized')
def github_authorized():
    response = github.authorized_response()

    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={}, error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['github_token'] = (response['access_token'], '')

    return redirect(url_for('dashboard'))


@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')


if __name__ == '__main__':
    app.run(debug=True)
