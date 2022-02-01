from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from flask_app.models.review import Review


class Landlord:
    def __init__(self, data):
        self.id = data['id']
        self.user = User.get_user_by_id({'id': data['user_id']})
        self.name = data['name']
        self.address = data['address']
        self.reviews = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # retrives one landlord with reviews from DB, landlord row id needs to be provided
    @classmethod
    def get_landlord_by_id(cls, data):
        query = "SELECT * FROM landlords JOIN reviews ON landlords.id=landlord_id JOIN users ON reviews.user_id=users.id WHERE landlords.id=%(id)s"
        landlord_db = connectToMySQL('landlord').query_db(query, data)
        landlord_cls = Landlord(landlord_db[0])
        
        for data in landlord_db:
            review_data = {
                'id': data['reviews.id'],
                'landlord_id': data['landlord_id'],
                'text': data['text'],
                'created_at': data['reviews.created_at'],
                'updated_at': data['reviews.updated_at'],
                'user_data': {
                    'id': data['users.id'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email'],
                    'nickname': data['nickname'],
                    'password': data['password'],
                    'created_at': data['users.created_at'],
                    'updated_at': data['users.updated_at']
                }
            }
            landlord_cls.reviews.append(Review(review_data))
        return landlord_cls

    # get all landlords
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM landlords;"
        results = connectToMySQL('landlord').query_db(query)
        all_landlords = []
        for row in results:
            all_landlords.append(cls(row))
        return all_landlords

    # method for adding landlord
    @classmethod
    def add_landlord(cls, data):
        query = "INSERT INTO landlords (name, user_id, address) VALUES (%(name)s, %(user_id)s, %(address)s);"
        result = connectToMySQL('landlord').query_db(query, data)
        return result


    # method for adding ratings
    @classmethod
    def add_rating(cls, data):
        query = "INSERT INTO ratings (landlord_id, user_id, rating) VALUES (%(landlord_id)s, %(user_id)s, %(rating)s);"
        result = connectToMySQL('landlord').query_db(query, data)
        return result

    # static method for validating landlord info flashes messages for incorrect or incomplete data
    # takes in form as an argument
    # returns True if form is correct otherwise returns False
    @staticmethod
    def validate_landlord_info(form):
        is_valid = True
        if len(form['name']) <= 0:
            is_valid = False
            flash("Review text can`t be empty.", 'landlord-error')
        if len(form['address']) <= 0:
            is_valid = False
            flash("Landlord address is required", 'landlord-error')
        return is_valid