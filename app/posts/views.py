import json
from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, session
from .forms import PostForm
from datetime import datetime
import json
import os

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
        posts = load_posts()
        new_post = {
            "id": len(posts) + 1,
            "title": form.title.data,
            "content": form.content.data,
            "category": form.category.data,
            "is_active": form.is_active.data,
            "publication_date": form.publish_date.data.strftime('%Y-%m-%d'),
            "author": session.get('username', 'Anonymous')  
        }
        posts.append(new_post)
        save_posts(posts)
        flash('Post added successfully!', 'success')
        return redirect(url_for('posts.view_posts'))
    return render_template('add_post.html', form=form)


@post_bp.route('/posts')
def view_posts():
    posts = load_posts()
    return render_template('posts.html', posts=posts)

@post_bp.errorhandler(404)
def page_not_found(error):

    return render_template('404.html'), 404

@post_bp.route('/posts')
def get_posts():
    try:
        with open(POSTS_FILE, 'r') as f:
            posts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        posts = []

    return render_template("posts.html", posts=posts)

@post_bp.route('/posts/<int:id>')
def detail_post(id):
    try:
        with open(POSTS_FILE, 'r') as f:
            posts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        abort(404)
    
    post = next((post for post in posts if int(post["id"]) == id), None)
    if post is None:
        abort(404)
    
    return render_template("detail_post.html", post=post)
