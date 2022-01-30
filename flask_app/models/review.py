from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User


class Review:
    def __init__(self, data):
        self.id = data['id']
        self.user = User.get_user_by_id({'id': data['id']})
        self.landlord_id = data['lendlord_id']
        self.text = data['text']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']