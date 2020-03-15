from flask import (
    Blueprint, flash, g, render_template, request, redirect, url_for, abort
)

from flaskr.view.auth import login_required
from flaskr.db import insert_db, query_db

bp = Blueprint('blog', __name__, url_prefix='/')


@bp.route('/')
def index():
    posts = query_db(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    )
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            insert_db(
                'INSERT INTO post (title, body, author_id) '
                'VALUES (%s, %s, %s)', (title, body, g.user['id'])
            )
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = query_db(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = %s', (id,)
    )[0]

    if post is None:
        abort(404, "Post id {} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            insert_db(
                'UPDATE post SET title = %s, body = %s'
                ' WHERE id = %s',
                (title, body, id)
            )
            return redirect(url_for('blog.article', id=id))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    insert_db('DELETE FROM post WHERE id = %s', (id,))
    return redirect(url_for('blog.index'))


@bp.route('/article/<int:id>')
def article(id):
    post = get_post(id, check_author=False)
    comments = get_comment(id)
    return render_template("blog/article.html", post=post, comments=comments)


@bp.route('/<int:id>/comment', methods=('POST',))
@bp.route('/<int:id>/<int:reply_to>/comment')
@login_required
def comment(id):
    body = request.form['body']
    reply_to = request.form['reply_to']
    insert_db(
        'INSERT INTO comment (reviewer_id, post_id, body, reply_to)'
        'VALUES (%s, %s, %s, %s) ', (g.user['id'], id, body, reply_to)
    )
    return redirect(url_for('blog.article', id=id))


def get_comment(id):
    comments = query_db(
        'SELECT username, body, created'
        ' FROM comment c JOIN user u ON c.reviewer_id = u.id'
        ' WHERE c.post_id = %s ORDER BY created DESC',
        (id))

    return comments
