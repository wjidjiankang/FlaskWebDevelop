from datetime import datetime
from flask import render_template, session, redirect, url_for, abort, request, current_app,flash
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
        return redirect(url_for('main.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
            page=page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
    posts = pagination.items

    return render_template('index.html', form=form,posts=posts, pagination=pagination )
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
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    # print (user)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


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


@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
                not current_user.can(Permission.ADMIN):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)

