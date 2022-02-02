from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.landlord import Landlord
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user' in session:
        data = {
            'id': session['user']
        }
        active_user = User.get_user_by_id(data)
        return redirect('/profile/' + active_user.first_name + '/' + str(active_user.id))
    return render_template('register_login.html')

@app.route('/edit/profile')
def update_profile_view():
    if 'user' not in session:
        return redirect('/')
    data = {
        'id': session['user']
    }
    active_user = User.get_user_by_id(data)
    return render_template('update_profile.html', active_user=active_user)

@app.route('/profile/<string:name>/<int:id>')
def dashboard(name, id):
    if 'user' in session:
        data = {
            'id': session['user']
        }
        active_user = User.get_user_by_id(data)
        landlords_from_db = Landlord.get_all()
        return render_template('dashboard.html', user=active_user, landlords_from_db=landlords_from_db)
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
    route = '/profile/' + data['first_name']+'/'+ str(session['user'])
    return redirect(route)

@app.route('/login/validation', methods=['POST'])
def login():
    if User.validate_login(request.form):
        session['user'] = User.validate_login(request.form)
        route = '/profile/' + User.get_user_by_id({'id':session['user']}).first_name +'/'+ str(session['user'])
        return redirect(route)
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