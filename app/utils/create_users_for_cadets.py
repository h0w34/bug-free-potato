import random
import secrets

from app.users.models import User
from app.duties.models import Cadet

from random_username.generate import generate_username
from app import db

# Define the connection URL
connection_url = r"C:\Users\mew\Desktop\duties\app.db"

# Create the engine
'''engine = create_engine(connection_url)

Session = sessionmaker(bind=engine)
session = Session()'''


def assign_users_to_cadets():
    users_created_count = 0
    userless_cadets = Cadet.query.filter(Cadet.user == None).all()  # this must be as this
    userfull_cadets = Cadet.query.filter(Cadet.user != None).all()
    usernames = [c.user.username for c in userfull_cadets]

    for cadet in userless_cadets:
        # print('user:', cadet.user)
        username = generate_username()[0]

        while username in usernames:
            username = generate_username()[0]

        user = User()
        user.username = username.lower()
        user.email = 'default@email.who'
        random_password = secrets.token_hex(4)

        user.set_password('password')
        user.cadet = cadet
        user.avatar = f'avatar_{random.randint(1, 25)}.png'
        db.session.add(user)
        db.session.commit()
        usernames += username
        users_created_count += 1

    return users_created_count
