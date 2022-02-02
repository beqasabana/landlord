from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.controllers import users


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.nickname = data['nickname']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # inserts new user in DB
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, nickname, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(nickname)s, %(password)s);"
        user_id = connectToMySQL('landlord').query_db(query, data)
        return user_id

    # retrives one user from DB by ID
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        user = connectToMySQL('landlord').query_db(query, data)
        print(user)
        return cls(user[0])

    # retrives one user from DB by EMAIL
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        user = connectToMySQL('landlord').query_db(query, data)
        if user:
            return cls(user[0])
        return False

    # retrives all users form DB
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        users_in_db = connectToMySQL('landlord').query_db(query)
        users_cls = []
        for user in users_in_db:
            users_cls.append(cls(user))
        return users_cls

    # updates users info user ID needs to be provided with new data
    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, nickname = %(nickname)s WHERE id = %(id)s;"
        result = connectToMySQL('landlord').query_db(query, data)
        return result

    # changes user password user ID needs to be provided with new password
    @classmethod
    def update_password(cls, data):
        query = "UPDATE users SET password = %(password)s WHERE id = %(id)s;"
        result = connectToMySQL('landlord').query_db(query, data)
        return result

    # email validation function
    @staticmethod
    def validate_email(form):
        is_valid = True
        if not EMAIL_REGEX.match(form['email']):
            flash("Invalid Email Address!", 'registration-error')
            is_valid = False
            return is_valid
        all_users_in_db = User.get_all()
        for one_user in all_users_in_db:
            if one_user.email == form['email']:
                flash("Email address already exists use different email address.", 'registration-error')
                is_valid = False
        return is_valid

    # user info and password validation function
    @staticmethod
    def validate_registation(form):
        is_valid = True
        if len(form['first_name']) < 3:
            is_valid = False
            flash("First Name must be at least 2 Characters.", 'registration-error')
        if len(form['last_name']) < 3:
            is_valid = False
            flash("Last Name must be at least 2 Characters.", 'registration-error')
        is_valid = User.validate_email(form)
        if len(form['password']) < 8:
            flash("Password is too short. Password should be at least 8 characters.", 'registration-error')
            is_valid = False
            return is_valid
        if form['password'] != form['password-conf']:
            flash("Password does not match.", 'registration-error')
            is_valid = False
        return is_valid

    # loging validation function if user provides correct email and password user ID is returned
    @staticmethod
    def validate_login(form):
        is_valid = True
        data = {
            'email': form['email']
        }
        user = User.get_user_by_email(data)
        if not user:
            is_valid = False
            flash("Invalid Email Address or Password.", 'login-error')
            return is_valid
        if not users.bcrypt.check_password_hash(user.password, form['password']):
            is_valid = False
            flash("Invalid Email Address or Password.", 'login-error')
            return is_valid
        return user.id


    # does not work properly needs to be reworked
    @staticmethod
    def validate_update(form):
        is_valid = True
        if len(form['first_name']) < 3:
            is_valid = False
            flash("First Name must be at least 2 Characters.", 'registration-error')
        if len(form['last_name']) < 3:
            is_valid = False
            flash("Last Name must be at least 2 Characters.", 'registration-error')
        is_valid = User.validate_email(form)
        return is_valid

    # validates password change checks old password and new password strength
    @staticmethod
    def validate_password_change(form, user=None):
        is_valid = True
        if not users.bcrypt.check_password_hash(user.password, form['old_password']):
            is_valid = False
            flash("Old Password is Wrong.", 'password-error')
            return is_valid
        if len(form['new_password']) < 8:
            flash("Password is too short. Password should be at least 8 characters.", 'password-error')
            is_valid = False
            return is_valid
        if form['new_password'] != form['conf_new_password']:
            flash("Password does not match.", 'password-error')
            is_valid = False
            return is_valid
        return user.id