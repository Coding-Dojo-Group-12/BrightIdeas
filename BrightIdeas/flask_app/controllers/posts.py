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

@app.route("/posts/<int:id>/edit_post_in_db", methods=["POST"])
def edit_idea_in_db(id):
    if "user_id" not in session:
        return redirect("/")
    if not Post.validate_post(request.form):
        return redirect(f"/edit/post/{id}")
    data = {
        "content" : request.form["content"],
        "id": id,
    }
    Post.update(data)
    return redirect(f"/show/post/{id}")



@app.route('/show/post/<int:id>')
def show_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : id
    }
    userData = {
        'id' : session['user_id']
    }
    return render_template('showPost.html', user=User.get_by_id(data), post=Post.get_one_post(data))

@app.route("/edit/post/<int:id>")
def edit_post(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id
    }
    return render_template("editPost.html", user=User.get_by_id(data), post = Post.get_one_post(data))

@app.route('/delete/post/<int:id>')
def delete_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : id
    }
    Post.delete(data)
    return redirect('/dashboard')