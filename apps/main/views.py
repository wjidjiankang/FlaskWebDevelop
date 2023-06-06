from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm,PostForm
from .. import db
from ..models import User, Permission,Post
from flask_login import current_user,login_required
from ..decorators import admin_required, permission_required



@main.route('/', methods=['GET', 'POST'])
def index():
    # name = None
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', form=form,posts=posts )
        # old_name = session.get('name')
        # if old_name is not None and old_name != form.name.data:
        #     flash('Looks like you have changed your name!')
        # session['name'] = form.name.data
        # return redirect(url_for('index'))
        # name = form.name.data
        # form.name.data = ''
    # return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'))


# @apps.route('/user/')
@main.route('/user/<username>/')
def user(username=None):
    user = User.query.filter_by(username=username).first_or_404()
    # print (user)
    return render_template('user.html', user=user)


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"

@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "For comment moderators!"

