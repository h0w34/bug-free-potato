from datetime import datetime, timedelta
import random
from .models import Duty, Cadet, DutyType, Location, ReserveCadetDuty
from app import db


# mock generation
# TODO: actually implement generation
def generate_schedule(start_date, end_date, location_ids=None, duty_type_ids=None):
    duties_count = 0
    cadet_ids = [cadet.id for cadet in Cadet.query.all()]

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    location_ids = location_ids if location_ids else [location.id for location in Location.query.all()]

    for date in [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]:
        # iterate over locations
        # location_ids_local = location_ids if location_ids else [location.id for location in Location.query.all()]
        for location_id in location_ids:
            # print(f'--------\ncurrent location id is {location_id}!')
            # check if the date is already occupied (may check 'archived' col or create a separate schedule table)
            duty = Duty.query.join(Duty.duty_type).filter(Duty.date == date,
                                                          DutyType.location_id == location_id).first()
            # print(f'duty for the {date} is {duty}!')
            if duty is None:
                # get all the types for location if none provided
                # print(f'BEFORE BEFORE: duty type ids for the location {location_id}: {duty_type_ids}')
                local_duty_type_ids = duty_type_ids if duty_type_ids else Location.query.get(location_id).duty_type_ids
                # print(f'BEFORE: duty type ids for the location {location_id}: {duty_type_ids}')
                # select only those that belong to the location
                local_duty_type_ids = [duty_type_id for duty_type_id in local_duty_type_ids if duty_type_id in
                                       Location.query.get(location_id).duty_type_ids]
                for duty_type_id in local_duty_type_ids:
                    # print(f'AFTER: current duty_type_id is {duty_type_id}, location_id is {location_id}!')
                    cadet_roles_ids = []
                    duty_type_roles_ids = DutyType.query.get(duty_type_id).duty_roles_ids
                    cadet_ids = [cadet.id for cadet in Cadet.query.all()]
                    random_cadet_ids = random.sample(cadet_ids, len(duty_type_roles_ids))
                    for role_id, cadet_id in zip(duty_type_roles_ids, random_cadet_ids):
                        cadet_roles_ids.append((cadet_id, role_id))
                    Duty.create_duty(date, duty_type_id, cadet_roles_ids)
                    duties_count += 1

    if duties_count:
        update_reserves()
        return f'Created {duties_count} duties from {start_date} to {end_date}', 200
    else:
        return 'Failed. No duties created.', 400

    # ...


def delete_duties(start_date, end_date, location_ids=None, duty_type_ids=None):
    duties_count = 0
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    location_ids = location_ids if location_ids else [location.id for location in Location.query.all()]
    for date in [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]:
        # iterate over locations
        location_ids = location_ids if location_ids else [location.id for location in Location.query.all()]
        for location_id in location_ids:
            # get all the types for location if none provided
            duty_type_ids_local = duty_type_ids if duty_type_ids else Location.query.get(location_id).duty_type_ids
            # select only those that belong to the location
            duty_type_ids_local = [duty_type_id for duty_type_id in duty_type_ids_local if duty_type_id in
                                   Location.query.get(location_id).duty_type_ids]
            for duty_type_id in duty_type_ids_local:
                # duty type already belongs to a location
                duty = Duty.query.filter_by(date=date, duty_type_id=duty_type_id).first()
                if duty:
                    # duty.free_reserves()
                    db.session.delete(duty) # .delete_duty()
                    duties_count += 1

    if duties_count:
        update_reserves()
        return f'Deleted {duties_count} duties from {start_date.strftime("%Y-%m-%d")} to' \
               f' {end_date.strftime("%Y-%m-%d")}', 200
    else:
        return 'Failed to delete duties', 400

    # ...


# dummy updating -- random choice
def update_reserves(duty_ids: list = None, reserve_num=3):
    if duty_ids:
        duties = [Duty.query.filter_by(archived=False, id=duty_id).first() for duty_id in duty_ids]
    else:
        duties = Duty.query.filter_by(archived=False).all()

    cadet_ids = [cadet.id for cadet in Cadet.query.all()]
    print(f'Всего {len(cadet_ids)} cadet_ids!')
    reserves_update_count = 0
    duties_update_count = 0

    for duty in duties:
        cadet_ids_local = cadet_ids.copy()
        #print(f'Всего {len(cadet_ids_local)} LOCAL cadet_ids!')
        local_duties_update_count = 0
        duty_role_ids = duty.duty_type.duty_roles_ids
        for role_id in duty_role_ids:
            # get reserves for the role
            reserves = (
                ReserveCadetDuty.query
                .filter(ReserveCadetDuty.duty_id == duty.id, ReserveCadetDuty.duty_role_id == role_id)
                .order_by(ReserveCadetDuty.priority)
                .all()
            )
            if len(reserves) == reserve_num:
                continue
            # Shift priorities for existing reserves
            for i, reserve in enumerate(reserves):
                reserve.priority = i + 1
                db.session.add(reserve)

            # Add missing reserves
            missing_count = reserve_num - len(reserves)
            for _ in range(missing_count):
                cadet_id = random.choice(cadet_ids_local)
                cadet_ids_local.remove(cadet_id)
                new_reserve = ReserveCadetDuty(
                    duty_id=duty.id,
                    duty_role_id=role_id,
                    cadet_id=cadet_id,
                    priority=len(reserves) + 1
                )
                db.session.add(new_reserve)
                reserves.append(new_reserve)
                local_duties_update_count += 1

        reserves_update_count += local_duties_update_count
        if local_duties_update_count:
            duties_update_count += 1

    db.session.commit()
    print(f'updated {reserves_update_count} reserves in {duties_update_count} duties')


def update_schedule():
    ...


def add_schedule():
    ...
