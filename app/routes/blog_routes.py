from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import Blog
from flask_cors import CORS


blog_bp = Blueprint('blog', __name__)
CORS(blog_bp)

@blog_bp.route('/')
def index():
    blogs = Blog.query.all()
    blog_list = []
    
    for blog in blogs:
        blog_data = {
            "id": blog.id,
            "title": blog.title,
            "content": blog.content,
            "author_id": blog.user_id,
            "created_at": blog.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(blog, 'created_at') else None
        }
        blog_list.append(blog_data)
    
    return jsonify({"blogs": blog_list}), 200


@blog_bp.route('/dashboard')
@login_required
def dashboard():
    blogs = Blog.query.filter_by(user_id=current_user.id).all()
    blog_list = []
    
    for blog in blogs:
        blog_data = {
            "id": blog.id,
            "title": blog.title,
            "content": blog.content,
            "created_at": blog.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(blog, 'created_at') else None
        }
        blog_list.append(blog_data)
    
    return jsonify({
        "user_id": current_user.id,
        "username": current_user.username,
        "blogs": blog_list
    }), 200


@blog_bp.route('/create', methods=['POST'])
@login_required
def create_blog():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No input data provided"}), 400
        
    title = data.get('title')
    content = data.get('content')
    
    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400
    
    blog = Blog(title=title, content=content, author=current_user)
    db.session.add(blog)
    db.session.commit()
    
    return jsonify({
        "message": "Blog created successfully",
        "blog_id": blog.id,
        "title": blog.title
    }), 201


@blog_bp.route('/edit/<int:id>', methods=['GET', 'PUT'])
@login_required
def edit_blog(id):
    blog = Blog.query.get_or_404(id)
    
    if blog.author != current_user:
        return jsonify({"error": "Unauthorized access"}), 403
    
    if request.method == 'GET':
        blog_data = {
            "id": blog.id,
            "title": blog.title,
            "content": blog.content,
            "created_at": blog.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(blog, 'created_at') else None
        }
        return jsonify({"blog": blog_data}), 200
        
    elif request.method == 'PUT':
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No input data provided"}), 400
            
        blog.title = data.get('title', blog.title)
        blog.content = data.get('content', blog.content)
        db.session.commit()
        
        return jsonify({
            "message": "Blog updated successfully",
            "blog_id": blog.id
        }), 200


@blog_bp.route('/delete/<int:id>', methods=['DELETE'])
@login_required
def delete_blog(id):
    blog = Blog.query.get_or_404(id)
    
    if blog.author != current_user:
        return jsonify({"error": "Unauthorized access"}), 403
        
    db.session.delete(blog)
    db.session.commit()
    
    return jsonify({
        "message": "Blog deleted successfully"
    }), 200


@blog_bp.route('/blog/<int:id>', methods=['GET'])
def view_blog(id):
    blog = Blog.query.get_or_404(id)
    
    author = blog.author.username if blog.author else "Unknown"
    
    blog_data = {
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "author": author,
        "created_at": blog.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(blog, 'created_at') else None
    }
    
    return jsonify({"blog": blog_data}), 200
