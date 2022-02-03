from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User


class Review:
    def __init__(self, data):
        self.id = data['id']
        self.user = User(data['user_data'])
        self.landlord_id = data['landlord_id']
        self.rating = data['rating']
        self.text = data['text']
        self.file_location = data['file_location']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # returns inserted row id or False if something goes wrong
    @classmethod
    def save(cls, data):
        query = "INSERT INTO reviews (landlord_id, user_id, rating, text, file_location) VALUES (%(landlord_id)s, %(user_id)s, %(rating)s, %(text)s, %(file_location)s);"
        review_id = connectToMySQL('landlord').query_db(query, data)
        return review_id

    # takes in the form and returns True or False with flashed messages
    @staticmethod
    def validate_review(form):
        is_valid = True
        if len(form['text']) <= 0:
            is_valid = False
            flash("Cant leave empty review.", 'review-error')
        return is_valid