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
        self.avg_rating = 0
        # self.reviews = Review.get_all_for_landlord({'landlord_id': self.id})
        self.reviews = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def get_average_rating(self):
        all_reviews = self.reviews
        total = 0
        num_reviews = len(all_reviews)
        print(num_reviews)
        for review in all_reviews:
            total+=review.rating
        avg = total
        return avg

    # retrives one landlord with reviews from DB, landlord row id needs to be provided
    @classmethod
    def get_landlord_by_id(cls, data):
        query = "SELECT * FROM landlords LEFT JOIN reviews ON landlords.id=landlord_id LEFT JOIN users ON reviews.user_id=users.id WHERE landlords.id=%(id)s"
        landlord_db = connectToMySQL('landlord').query_db(query, data)
        landlord_cls = Landlord(landlord_db[0])
        rating_count = 0
        sum_of_ratings = 0
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
            rating_count += 1
            sum_of_ratings += data['rating']
            landlord_cls.reviews.append(Review(review_data))
        landlord_cls.avg_rating = round((sum_of_ratings/rating_count))
        return landlord_cls

    # get all landlords
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM landlords LEFT JOIN reviews ON landlords.id=reviews.landlord_id;"
        results = connectToMySQL('landlord').query_db(query)
        if len(results) == 0:
            return results
        all_landlords = []
        # for row in results:
        #     all_landlords.append(cls(row))
        loop_position = 0
        rating_count = 0
        sum_of_ratings = 0
        all_landlords.append(Landlord(results[0]))
        rating_count += 1
        sum_of_ratings += results[0]['rating']
        results.pop(0)
        for row in results:
            if all_landlords[-1].id != row['id']:
                all_landlords[-1].avg_rating = round(sum_of_ratings/rating_count)
                rating_count = 0
                sum_of_ratings = 0
                all_landlords.append(Landlord(row))
            loop_position += 1
            rating_count += 1
            try:
                sum_of_ratings += row['rating']
            except TypeError:
                sum_of_ratings += 0
            if loop_position >= len(results):
                all_landlords[-1].avg_rating = round(sum_of_ratings/rating_count)
        return all_landlords

    # delete landlord from db needs row id
    @classmethod
    def delete(cls, data):
        query_review = "DELETE FROM reviews WHERE landlord_id=%(id)s"
        query_landlord = "DELETE FROM landlords WHERE id=%(id)s"
        connectToMySQL('landlord').query_db(query_review, data)
        connectToMySQL('landlord').query_db(query_landlord, data)
        return

    # update/edit landlord query need name address and landlord row id to update 
    @classmethod
    def update(cls, data):
        query = "UPDATE landlords SET name=%(name)s, address=%(address)s WHERE id=%(id)s;"
        connectToMySQL('landlord').query_db(query, data)
        return

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