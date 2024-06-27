from ..duties.models import Cadet
from ..users.models import User
from random_username.generate import generate_username
from app import db
import secrets
import string


def generate_user(email: str = None):
    cadets_with_users = Cadet.query.filter(Cadet.user != None).all()
    usernames = [c.user.username for c in cadets_with_users]

    username = generate_username()[0]
    while username in usernames:
        username = generate_username()[0]

    user = User()
    user.username = username.lower()

    user.email = email if email else None
    random_password = generate_password()

    user.set_password(random_password)
    user.avatar = 'no_avatar.png'
    '''db.session.add(user)
    db.session.commit()'''

    return user, random_password


def generate_password(length=12):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password
