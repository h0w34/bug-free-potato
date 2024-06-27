import random
import secrets

from app.users.models import User
from app.duties.models import Cadet, Group, Course, Faculty

from random_username.generate import generate_username
from app import db

# Define the connection URL
connection_url = r"C:\Users\mew\Desktop\duties\app.db"

# Create the engine
'''engine = create_engine(connection_url)

Session = sessionmaker(bind=engine)
session = Session()'''

def generate_cadets_for_group(group_id, num=30):
    for _ in range(num):
        cadet = Cadet()
        ...
        # TODO...




def generate_cadets_with_users(cadets_per_group: int=None, group_ids: list=None, course_ids: list=None, faculty_ids: list=None):
    group_ids = group_ids if group_ids else [group.id for group in Group.query.all()]
    course_ids = course_ids if course_ids else [course.id for course in Course.query.all()]
    faculty_ids = faculty_ids if faculty_ids else [faculty.id for faculty in Faculty.query.all()]

    for faculty_id in faculty_ids:
        for course in course_ids:
            for group in group_ids:
                ...
                # TODO...


def generate_users_for_existing_cadets():
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
        """user.email = 'default@email.who'"""
        random_password = secrets.token_hex(4)

        user.set_password('password')
        user.cadet = cadet
        user.avatar = f'avatar_{random.randint(1, 25)}.png'
        db.session.add(user)
        db.session.commit()
        usernames += username
        users_created_count += 1

    return users_created_count
