import this
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.landlord import Landlord
from flask_app.models.review import Review
from flask_bcrypt import Bcrypt
from datetime import datetime

@app.route('/create/review/<int:landlord_id>', methods = ['POST'])
def create_review_for_landlord(landlord_id):
    active_user = User.get_user_by_id({'id': session['user']})
    print("hiiiiii", request.form)
    try:
        review_data = {
            'landlord_id': landlord_id,
            'user_id': session['user'],
            'rating': request.form['rating'],
            'text': request.form['review']
        }
    except KeyError:
        review_data = {
            'landlord_id': landlord_id,
            'user_id': session['user'],
            'rating': 0,
            'text': request.form['review']
        }
    review_added = Review.save(review_data)
    return redirect('/profile/' + active_user.first_name + '/' + str(active_user.id))
