from facebook import get_user_from_cookie, GraphAPI
from flask import g, flash, render_template, redirect, request, session, url_for

from app import app, db
from config import FB_APP_ID, FB_APP_NAME, FB_APP_SECRET
from .models import User

@app.route('/')
def index():
    return render_template('index.html', app_id=FB_APP_ID, app_name=FB_APP_NAME, user=g.user)

    # if g.user:
    #     return render_template('index.html', app_id=FB_APP_ID,
    #                            app_name=FB_APP_NAME, user=g.user)
    # return render_template('login.html', app_id=FB_APP_ID, name=FB_APP_NAME)

@app.route('/login')
def login():
    return render_template('login.html', app_id=FB_APP_ID, name=FB_APP_NAME)

@app.route('/logout')
def logout():
    """Log out the user from the application.
    Log out the user from the application by removing them from the
    session.  Note: this does not log the user out of Facebook - this is done
    by the JavaScript SDK.
    """
    session.pop('user', None)
    return redirect(url_for('index'))

@app.before_request
def get_current_user():
    if session.get('user'):
        g.user = session.get('user')
        return

    result = get_user_from_cookie(cookies=request.cookies, app_id=FB_APP_ID,
                                  app_secret=FB_APP_SECRET)

    if result:
        user = User.query.filter(User.id == result['uid']).first()
        if not user:
            graph = GraphAPI(result['access_token'])
            profile = graph.get_object('me')
            if 'link' not in profile:
                profile['link'] = ""
            user = User(id=str(profile['id']),
                        name=profile['name'],
                        profile_url=profile['link'],
                        access_token=result['access_token'])
            db.session.add(user)
        elif user.access_token != result['access_token']:
            user.access_token = result['access_token']
        session['user'] = dict(name=user.name, profile_url=user.profile_url,
                               id=user.id, access_token=user.access_token)
    db.session.commit()
    g.user = session.get('user', None)

@app.route('/user/<name>')
def user(name):
    user = User.query.filter_by(name=name).first()
    if user == None:
        flash('User %s not found.' % name)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',
                           user=user,
                           posts=posts)