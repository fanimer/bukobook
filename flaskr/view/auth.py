import functools

from flask import (Blueprint, flash, redirect, g, render_template, request, url_for, session)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import query_db, insert_db

bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif query_db('SELECT id FROM user WHERE username = %s', (username,)):
            error = 'User {} is already registered'.format(username)

        if error is None:
            if not insert_db('INSERT INTO user (username, password) VALUES (%s, %s)',
                             (username, generate_password_hash(password))):
                error = 'System error, please try again.'
            else:
                return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        try:
            user = query_db('SELECT * FROM user WHERE username = %s', (username,))[0]
        except IndexError:
            user = None
        if not user:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('space.personal', username=username))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = query_db('SELECT * FROM user WHERE id = %s', (user_id,))[0]


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view
