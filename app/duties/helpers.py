from .models import Duty
from app import db

def lock_duty(duty_id, user_id):
    duty = Duty.query.get(duty_id)
    if duty.locked and duty.locked_by != user_id:
        return False
    duty.locked = True
    duty.locked_by = user_id
    db.session.commit()
    return True

def unlock_duty(duty_id, user_id):
    duty = Duty.query.get(duty_id)
    if duty.locked and duty.locked_by == user_id:
        duty.locked = False
        duty.locked_by = None
        db.session.commit()
        return True
    return False

def is_locked_by(duty_id, user_id):
    duty = Duty.query.get(duty_id)
    return duty.locked and duty.locked_by == user_id

