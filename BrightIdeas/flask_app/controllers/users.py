from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data = {
        'firstName' : request.form['firstName'],
        'lastName' : request.form['lastName'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['userId'] = id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid email', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid password', 'login')
        return redirect('/')
    session['userId'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'userId' not in session:
        return redirect('/logout')
    data ={
        'id': session['userId']
    }
    return render_template('dashboard.html',user=User.get_by_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')