from flask import Blueprint, request, render_template
from flask_login import login_required
from blog_project.models import Post


posts = Blueprint('posts', __name__)  # план


@posts.route('/allposts')
@login_required
def allposts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('allposts.html', posts=posts)  # именован параметр posts= будет исп в шаблоне



