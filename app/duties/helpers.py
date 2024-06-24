from .models import Duty
from ..users.models import User
from app import db

def lock_duty(duty_id, username):
    duty = Duty.query.get(duty_id)
    user = User.get_by_username(username)
    if duty.locked and duty.locked_by != user.id:
        return False
    duty.locked = True
    duty.locked_by = user.id
    db.session.commit()
    return True

def unlock_duty(duty_id, username):
    duty = Duty.query.get(duty_id)
    user = User.get_by_username(username)
    if duty.locked and duty.locked_by == user.id:
        duty.locked = False
        duty.locked_by = None
        db.session.commit()
        return True
    return False

def is_locked_by(duty_id, username):
    duty = Duty.query.get(duty_id)
    user = User.get_by_username(username)
    return duty.locked and duty.locked_by == user.id

