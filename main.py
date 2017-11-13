from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flask import session as session_info

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from database_setup import Base, User, Post, Comment

import requests
import uuid
import hashlib
from functools import wraps

app = Flask(__name__, static_url_path='/static/*')

my_file = open("secret_key.txt", "r")
my_key = my_file.read()
my_file.close()

app.config['SECRET_KEY'] = my_key

engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + "," + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(",")
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


def get_user_id():
    if 'user_id' in session_info:
        return session_info['user_id']
    else:
        return None


def get_username():
    if 'username' in session_info:
        return session_info['username']
    else:
        return None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session_info:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@app.route('/front')
def main():
    user_id = get_user_id()
    posts = session.query(Post).order_by(desc(Post.created_date)).all()
    return render_template('front.html', posts=posts, user=user_id)


@app.route('/test')
def post_test():
    items = session.query(Post).order_by(desc(Post.created_date)).all()
    users = session.query(User).all()
    comments = session.query(Comment).all()
    return render_template('test-post.html', items=items, users=users, comments=comments)


@app.route('/newpost', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        new_post = Post(user_id=session_info['user_id'], title=request.form['title'], content=request.form['content'])
        session.add(new_post)
        session.commit()
        return redirect(url_for('post_test'))
    else:
        user_id = get_user_id()
        return render_template('newpost.html', user=user_id)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    if request.method == 'POST':
        try:
                user_id = session_info['user_id']
        except:
                return redirect(url_for('login'))

        new_comment = Comment(user_id=user_id, post_id=post_id, content=request.form['content'])
        session.add(new_comment)
        session.commit()
        return redirect(url_for('post', post_id=post_id))
    else:
        user_id = get_user_id()
        post = session.query(Post).get(post_id)
        comments = session.query(Comment).filter(Comment.post_id == post_id).all()
        if post:
                return render_template('post.html', post=post, comments=comments, user=user_id)
        else:
                return redirect(url_for('post_test'))


@app.route('/post/<int:post_id>/delete', methods=['GET'])
@login_required
def delete_post(post_id):
    post = session.query(Post).get(post_id)
    comments = session.query(Comment).filter(Comment.post_id == post_id).all()
    if post:
        if post.user_id == user_id:
            session.delete(post)
            for i in range(len(comments)):
                session.delete(comments[i])
            session.commit()
        return redirect(url_for('post_test'))
    else:
        return redirect(url_for('post_test'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
            # See if user already exists
            try:
                user = session.query(User).filter(User.name == request.form['username']).one()
                if user:
                    return "User already exists"
            except (NoResultFound, MultipleResultsFound) as e:
                pass

            new_user = User(name=request.form['username'], password_hash=hash_password(request.form['password']))
            session.add(new_user)
            session.commit()
            return redirect(url_for('post_test'))
	else:
            return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		try:
                    user = session.query(User).filter(User.name == request.form['username']).one()
		except MultipleResultsFound:
                    return 'Multiple results found. Contact system administrator. (This should not happen.)'
		except NoResultFound:
                    user = None
                if user and check_password(user.password_hash, request.form['password']):
                    session_info['username'] = user.name
                    session_info['user_id'] = user.id
                    return redirect(url_for('post_test'))
		else:
                    return redirect(url_for('login'))
		# return str(session_info['username'])
	else:
		return render_template('login.html')


@app.route('/logout')
def logout():
    try:
	del session_info['username']
	del session_info['user_id']
    except:
        pass
    return redirect(url_for('main'))
