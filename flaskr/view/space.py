from flask import current_app, request, redirect, url_for, render_template, Blueprint, abort, g
from flaskr.db import insert_db, query_db

bp = Blueprint('space', __name__, url_prefix='/')


@bp.route('/personal/<username>')
def personal(username):
    posts = query_db(
        'SELECT title, body, created, p.id, author_id'
        ' FROM post p JOIN user u ON u.username = %s and p.author_id = u.id',
        (username,)
    )
    return render_template("space/personal.html", posts=posts)
