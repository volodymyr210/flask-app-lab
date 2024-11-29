from flask import Flask, request
from .models import Post
import json
from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, session
from .forms import PostForm
from datetime import datetime
import json
import os
from app import db  

POSTS_FILE = 'app/posts/posts.json'  


def load_posts():
    """Load posts from JSON file."""
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_posts(posts):
    """Save posts to JSON file."""
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f, indent=4)
        
@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    
    
    if form.validate_on_submit():
        
        title = form.title.data
        content = form.content.data
        is_active = form.is_active.data
        publish_date = form.publish_date.data
        category = form.category.data
        author = session.get('username', 'Anonymous')  
        
        
        post_new = Post(
            title=title,
            content=content,
            is_active=is_active,
            publish_date=publish_date,
            category=category,
            author=author
        )
        
        
        db.session.add(post_new)
        db.session.commit()
        
        flash(f'Post "{title}" added successfully!', 'success')
        return redirect(url_for('posts.get_posts')) 
    elif form.errors:
        flash(f"Enter the correct data in the form!", "danger")
   
    return render_template("add_post.html", form=form)



@post_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@post_bp.route('/posts')
def get_posts():
    posts = Post.query.order_by(Post.publish_date.desc()).all()  
    return render_template("posts.html", posts=posts)


@post_bp.route('/posts/<int:id>')
def detail_post(id):
    post = Post.query.get(id)
    if post is None:
        abort(404)
    
    return render_template("detail_post.html", post=post)

@post_bp.route('/posts/delete/<int:id>', methods=['GET'])
def delete_post(id):
    post = Post.query.get(id)
    if post is None:
        abort(404)

    db.session.delete(post)
    db.session.commit()
    flash(f'Post "{post.title}" has been deleted successfully!', 'success')
    return redirect(url_for('posts.get_posts'))

@post_bp.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)  
    form = PostForm(obj=post)  

    if request.method == 'GET':
        form.publish_date.data = post.publish_date

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        post.publish_date = form.publish_date.data  
        post.category = form.category.data
        post.author = session.get('username', 'Anonymous')  

        db.session.commit()  

        flash(f'Post "{post.title}" has been updated successfully!', 'success')
        return redirect(url_for('posts.get_posts'))  

    return render_template('edit_post.html', form=form, post=post)


