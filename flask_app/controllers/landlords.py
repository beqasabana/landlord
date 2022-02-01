from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.landlord import Landlord
from flask_app.models.review import Review
from flask_bcrypt import Bcrypt
from datetime import datetime

# Create a New Landlord
@app.route('/new/landlord')
def new_landlord():
    if 'user' not in session:
        return redirect('/logout')
    this_user = User.get_user_by_id({'id': session['user']})
    return render_template("add_landlord.html", user = this_user)

@app.route('/create/landlord', methods = ['POST'])
def create_landlord():
    # Create a Rating
    # Create a Review

    # Create Landlord with Rating and Reviews
    landlord_info = {
        'name': request.form['name'],
        'user_id': session['user'],
        'address': request.form['address'],
    }
    new_landlord_id = Landlord.add_landlord(landlord_info)
    this_user = User.get_user_by_id({'id': session['user']})
    return redirect('/profile/' + this_user.first_name +'/'+ str(session['user']))