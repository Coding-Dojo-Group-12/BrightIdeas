from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.post import Post
from flask_app.models.user import User
from flask_app.models.like import Like


@app.route('/create/post', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Post.validate_post(request.form):
        return redirect('/dashboard')
    data = {
        'content': request.form['content'],
        'likes': 0,
        'user_id': session['user_id']
    }
    Post.save(data)

    return redirect('/dashboard')



@app.route('/show/post/<int:id>')
def show_post(id):
    if 'userId' not in session:
        return redirect('/logout')
    data = {
        'id' : id
    }
    userData = {
        'id' : session['user_id']
    }
    return render_template('showPost.html', post=Post.get(data), user=User.get_by_id(userData))

@app.route('/delete/post/<int:id>')
def delete_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : id
    }
    Post.delete(data)
    return redirect('/dashboard')