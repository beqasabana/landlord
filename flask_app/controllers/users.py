from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.landlord import Landlord
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    data = {'id': 1}
    if 'user' in session:
        data = {
            'id': session['user']
        }
        active_user = User.get_user_by_id(data)
        return render_template('landing_page.html', active_user=active_user)
    return render_template('landing_page.html')

@app.route('/register')
def register_view():
    if 'user' in session:
        return redirect('/')
    return render_template('register.html')

@app.route('/edit/profile')
def update_profile_view():
    if 'user' not in session:
        return redirect('/')
    data = {
        'id': session['user']
    }
    active_user = User.get_user_by_id(data)
    return render_template('update_profile.html', active_user=active_user)

@app.route('/login')
def login_view():
    if 'user' in session:
        return redirect('/')
    return render_template('login.html')

@app.route('/profile/<string:name>/<int:id>')
def dashboard(name, id):
    if 'user' in session:
        data = {
            'id': session['user']
        }
        active_user = User.get_user_by_id(data)
        return render_template('profile.html', active_user=active_user)
    else:
        flash("You are not logged in!", 'not-loggedin')
        return redirect('/')

@app.route('/register/user', methods=['POST'])
def register_user():
    if not User.validate_registation(request.form):
        return redirect('/register')
    data = {
        'first_name': request.form['first_name'], 
        'last_name': request.form['last_name'], 
        'email': request.form['email'], 
        'password': bcrypt.generate_password_hash(request.form['password']),
        'nickname': request.form['nickname']
    }
    session['user'] = User.create(data)
    return redirect('/')

@app.route('/login/validation', methods=['POST'])
def login():
    if User.validate_login(request.form):
        session['user'] = User.validate_login(request.form)
        return redirect('/')
    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/update/user/<int:user_id>', methods=['POST'])
def update_profile(user_id):
    data = {
        'id': user_id,
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'nickname': request.form['nickname']
    }
    User.update_user(data)
    return redirect('/profile/' + request.form['first_name'] + request.form['last_name'] + '/' + str(user_id))

@app.route('/change/password')
def change_password_view():
    if 'user' not in session:
        return redirect('/')
    data = {
        'id': session['user']
    }
    active_user = User.get_user_by_id(data)
    return render_template('change_password.html', active_user=active_user)

@app.route('/changing/password', methods = ['POST'])
def change_password():
    user = User.get_user_by_id({
        'id': session['user']
    })
    if not User.validate_password_change(request.form, user):
        return redirect('/change/password')
    password_data = {
        'id': user.id,
        'password': bcrypt.generate_password_hash(request.form['new_password'])
    }
    User.update_password(password_data)
    return redirect('/profile' + '/' + user.first_name + user.last_name + '/' + str(user.id))