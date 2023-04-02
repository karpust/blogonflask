from flask import Blueprint, request, render_template, flash, redirect, \
    url_for, abort
from flask_login import login_required, current_user
from blog_project.models import Post
from blog_project.posts.forms import PostForm
from blog_project import db


posts = Blueprint('posts', __name__)  # план


@posts.route('/allposts')
@login_required
def allposts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('allposts.html', posts=posts)  # именован параметр posts= будет исп в шаблоне


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Ваш пост создан', 'success')
        return redirect(url_for('posts.allposts'))  # достает урл из вьюшки: redirect('/allposts')
    return render_template('create_post.html', title='Новый пост', form=form, legend='Новый пост')


@posts.route('/post/<int:post_id>', methods=['GET'])
@login_required
def detail_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('detail_post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Ваш пост обновлен', 'success')
        return redirect(url_for('posts.detail_post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        return render_template('create_post.html', form=form, title='Обновление поста',
                               legend='Обновление поста')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Ваш пост был удален!', 'success')
    return redirect(url_for('posts.allposts'))




