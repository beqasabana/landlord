from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User


class Landlord:
    def __init__(self, data):
        self.id = data['id']
        self.user = User.get_user_by_id({'id': data['user_id']})
        self.name = data['name']
        self.address = data['address']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']