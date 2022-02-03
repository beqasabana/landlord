from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User


class Review:
    def __init__(self, data):
        self.id = data['id']
        self.landlord_id = data['landlord_id']
        self.user = data['user_id']
        self.rating = data['rating']
        self.text = data['text']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # returns inserted row id or False if something goes wrong
    @classmethod
    def save(cls, data):
        query = "INSERT INTO reviews (landlord_id, user_id, rating, text) VALUES (%(landlord_id)s, %(user_id)s, %(rating)s, %(text)s);"
        review_id = connectToMySQL('landlord').query_db(query, data)
        return review_id

    @classmethod
    def get_all_for_landlord(cls, data):
        query = "SELECT * FROM reviews WHERE landlord_id = %(landlord_id)s;"
        results = connectToMySQL('landlord').query_db(query, data)
        reviews_for_landlord = []
        for row in results:
            reviews_for_landlord.append(cls(row))
        return reviews_for_landlord

    # takes in the form and returns True or False with flashed messages
    @staticmethod
    def validate_review(form):
        is_valid = True
        if len(form['text']) <= 0:
            is_valid = False
            flash("Cant leave empty review.", 'review-error')
        return is_valid