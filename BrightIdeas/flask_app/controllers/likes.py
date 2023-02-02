from flask import render_template, redirect, session, request
from flask_app import app
from flask_app.models.post import Post
from flask_app.models.user import User
from flask_app.models.like import Like

@app.route('/like', methods=['POST'])
def like():
    if 'user_id' not in session:
        return redirect ('/logout')
    data = {
        'post_id' : request.form['post_id'],
        'user_id' : session['user_id']
    }
    Like.save(data)
    return redirect('/dashboard')