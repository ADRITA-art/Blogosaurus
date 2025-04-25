from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .. import db
from ..models import Blog

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    blogs = Blog.query.all()
    return render_template('index.html', blogs=blogs)


@blog_bp.route('/dashboard')
@login_required
def dashboard():
    blogs = Blog.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', blogs=blogs)


@blog_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_blog():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog = Blog(title=title, content=content, author=current_user)
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('blog.dashboard'))
    return render_template('create_blog.html')


@blog_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_blog(id):
    blog = Blog.query.get_or_404(id)
    if blog.author != current_user:
        return redirect(url_for('blog.dashboard'))
    if request.method == 'POST':
        blog.title = request.form['title']
        blog.content = request.form['content']
        db.session.commit()
        return redirect(url_for('blog.dashboard'))
    return render_template('edit_blog.html', blog=blog)


@blog_bp.route('/delete/<int:id>')
@login_required
def delete_blog(id):
    blog = Blog.query.get_or_404(id)
    if blog.author != current_user:
        return redirect(url_for('blog.dashboard'))
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('blog.dashboard'))


@blog_bp.route('/blog/<int:id>')
def view_blog(id):
    blog = Blog.query.get_or_404(id)
    return render_template('view_blog.html', blog=blog)
