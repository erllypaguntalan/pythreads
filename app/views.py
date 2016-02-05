from facebook import get_user_from_cookie, GraphAPI
from flask import g, flash, render_template, redirect, request, session, url_for

from app import app, db
from config import FB_APP_ID, FB_APP_NAME, FB_APP_SECRET
from .models import User



@app.route('/')
def index():
    if g.user:
        return render_template('index.html', app_id=FB_APP_ID,
                                app_name=FB_APP_NAME, user=g.user)
            
    return render_template('index.html', app_id=FB_APP_ID, name=FB_APP_NAME)


@app.before_request
def before_request():
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


            user = User(id=str(profile['id']), name=profile['name'],
                        access_token=result['access_token'],
                        nickname=profile['name'].split(' ')[0])
            db.session.add(user)
        elif user.access_token != result['access_token']:
            user.access_token = result['access_token']

        session['user'] = dict(name=user.name, id=user.id, access_token=user.access_token,
                                nickname=user.nickname)
    db.session.commit()
    g.user = session.get('user', None)



@app.route('/login')
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html', app_id=FB_APP_ID, name=FB_APP_NAME)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))



@app.route('/user/<nickname>')
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',
                           user=user,
                           posts=posts)