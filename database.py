from mongoengine import *
from datetime import datetime
import uuid

# Define the user schema
class User(Document):
    username = StringField(required=True, unique=True, min_length=3, max_length=20)
    password = StringField()
    internal_id = StringField()
    socket = StringField(default="null")
    latest_connection = DateTimeField(default=datetime.utcnow)
    first_connection = DateTimeField(default=datetime.utcnow)

def init_user(data):
    try:
        new_user = User(
            username=data['username'],
            password=data['password'],
            internal_id=str(uuid.uuid4()),
            socket='null',
            latest_connection=datetime.utcnow(),
            first_connection=datetime.utcnow()
        )
        new_user.save()
        return new_user
    except Exception as e:
        print('Error creating user')
        print(e)
        raise e

def get_user(username):
    user = User.objects(username=username).first()
    if user:
        return user
    else:
        return False
