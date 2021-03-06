# coding: utf-8

from flask import Flask
from flask import g, session, request, url_for, flash
from flask import redirect, render_template
from flask_oauthlib.client import OAuth
from TwitterApiAccess import TwitterApiAccess
from UnfollowCheck import UnfollowCheck

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

oauth = OAuth(app)

CONSUMER_KEY = 'Z6RhJkSMTOryXQBvAPlsD6Mcs'
CONSUMER_SECRET = 'OewfFfiFswQgzDirU2vdbmiIMrr7SXOCpeII83sbWlT8WsNODJ'

twitter = oauth.remote_app(
    'twitter',
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize'
)


@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']


@app.before_request
def before_request():
    g.user = None
    if 'twitter_oauth' in session:
        g.user = session['twitter_oauth']


@app.route('/')
def index():
    tweets = None
    unfollowers = None

    if g.user is not None:
        print(get_twitter_token())
        twitter_manager = TwitterApiAccess(CONSUMER_KEY, CONSUMER_SECRET, twitter, session)

        uc = UnfollowCheck(twitter_manager)
        unfollowers = uc.unfollowers
        print(type(unfollowers))
        print(unfollowers)
    return render_template('index.html', unfollowers=unfollowers)


@app.route('/tweet', methods=['POST'])
def tweet():
    if g.user is None:
        return redirect(url_for('login', next=request.url))
    status = request.form['tweet']
    if not status:
        return redirect(url_for('index'))
    resp = twitter.post('statuses/update.json', data={
        'status': status
    })

    if resp.status == 403:
        flash("Error: #%d, %s " % (
            resp.data.get('errors')[0].get('code'),
            resp.data.get('errors')[0].get('message'))
              )
    elif resp.status == 401:
        flash('Authorization error with Twitter.')
    else:
        flash('Successfully tweeted your tweet (ID: #%s)' % resp.data['id'])
    return redirect(url_for('index'))


@app.route('/unfollow')
def unfollow():
    user = request.args.get('user', '')
    flash("unfollow " + user)
    return redirect(url_for('index'))


@app.route('/follow')
def follow():
    user = request.args.get('user', '')
    flash("follow " + user)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    callback_url = url_for('oauthorized', next=request.args.get('next'))
    return twitter.authorize(callback=callback_url or request.referrer or None)


@app.route('/logout')
def logout():
    session.pop('twitter_oauth', None)
    return redirect(url_for('index'))


@app.route('/oauthorized')
def oauthorized():
    resp = twitter.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
    else:
        session['twitter_oauth'] = resp
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
