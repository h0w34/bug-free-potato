from sqlalchemy import Column, Boolean, Enum
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date, DateTime
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

from app import db


'''class ReplacementType(db.Model):
    __tablename__ = 'replacement_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)'''


'''class DocType(db.Model):
    __tablename__ = 'doc_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)'''


# document doesn't have to be related to a replacement
# can be added to a cadet from the userpage to exclude him from the schedule
class ReplacementDoc(db.Model):
    __tablename__ = "replacement_docs"

    def __init__(self, cadet_id, start_date, end_date, contents=None):
        self.cadet_id = cadet_id
        self.start_date = start_date
        self.end_date = end_date
        if contents:
            self.contents = contents

    # doc_type = ...
    id = Column(Integer, primary_key=True)
    cadet_id = Column(Integer, ForeignKey('cadets.id'))
    contents = Column(String(500))
    start_date = Column(Date)
    end_date = Column(Date)
    # for now, we don't implement the docTypes

    # image = ...
    replacement = relationship('DutyReplacement', back_populates='replacement_doc')


class DutyReplacement(db.Model):
    __tablename__ = "duty_replacements"
    id = Column(Integer, primary_key=True)
    duty_id = Column(Integer, ForeignKey('duties.id'), nullable=False)
    replaced_id = Column(Integer, ForeignKey('cadets.id'), nullable=False)
    replacing_id = Column(Integer, ForeignKey('cadets.id'), nullable=False)
    duty_role_id = Column(Integer, ForeignKey('duty_roles.id'), nullable=False)
    # replacement_type_id = Column(Integer, ForeignKey('replacement_types.id'))
    replacement_doc_id = Column(Integer, ForeignKey('replacement_docs.id'), nullable=True) # either a doc or other reason
    # cadet_id = Column(Integer, ForeignKey('cadets.id'))
    # replacement_doc_id = Column(Integer, ForeignKey('replacement_docs.id'), nullable=False)
    commentary = Column(String(300))
    # start_date = Column(Date)
    # end_date = Column(Date)
    creation_date = Column(DateTime, default=datetime.now(), nullable=False)
    duty_role = relationship('DutyRole')
    replaced_cadet = relationship('Cadet', foreign_keys='DutyReplacement.replaced_id')
    replacing_cadet = relationship('Cadet', foreign_keys='DutyReplacement.replacing_id')

    replacement_doc = relationship('ReplacementDoc', back_populates='replacement')
    duty = relationship('Duty', back_populates='cadet_replacements')

    def __init__(self, duty_id, replaced_id, replacing_id, duty_role_id, replacement_doc_id=None, commentary=None):
        self.duty_id = duty_id
        self.replaced_id = replaced_id
        self.replacing_id = replacing_id
        self.duty_role_id = duty_role_id
        if replacement_doc_id:
            self.replacement_doc_id = replacement_doc_id
        if commentary:
            self.commentary = commentary

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.creation_date,
            'replaced_cadet': self.replaced_cadet.to_dict(),
            'replacing_cadet': self.replacing_cadet.to_dict(),
            'commentary': self.commentary,
            'replacement_doc_id': self.replacement_doc_id,
            'duty_role': self.duty_role.to_dict()
        }


class Location(db.Model):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    faculties = relationship('Faculty', back_populates='location')

    duty_types = relationship('DutyType')

    @property
    def duty_type_ids(self):
        return [duty_type.id for duty_type in self.duty_types]

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }


class DutyRole(db.Model):
    __tablename__ = "duty_roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    duty_type_id = Column(Integer, ForeignKey('duty_types.id'), nullable=False)  # each duty belongs to a dutyType

    duty_type = relationship('DutyType', back_populates='duty_roles')
    cadet_duties = relationship('CadetDuty', back_populates='duty_role')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


# we assume that the role ids are incremental correspondingly to their order in a duty
# i.e. if the first added role is КПП4, then it will stay like that
class DutyType(db.Model):
    __tablename__ = "duty_types"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    duty_roles = relationship('DutyRole', back_populates='duty_type')  # one duty can have multiple duty_roles
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    description = Column(String(250))

    location = relationship('Location')

    @property
    def duty_roles_ids(self):
        return [role.id for role in self.duty_roles]

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'location': self.location.to_dict(),
            'duty_roles': [role.to_dict() for role in self.duty_roles]
        }

    def to_table_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'duty_roles': [role.to_dict() for role in self.duty_roles]
        }


class Duty(db.Model):
    __tablename__ = "duties"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    duty_type_id = Column(Integer, ForeignKey('duty_types.id'), nullable=False)
    female_duty = Column(Boolean, default=0)
    archived = Column(Boolean, default=False)

    duty_type = relationship('DutyType')
    cadets = relationship('Cadet', secondary='cadet_duty', back_populates='duties')
    cadet_duties = relationship('CadetDuty', back_populates='duty', cascade='all, delete-orphan')

    reserve_cadet_duties = relationship('ReserveCadetDuty', back_populates='duty', cascade='all, delete-orphan')
    cadet_replacements = relationship('DutyReplacement', back_populates='duty', cascade='all, delete-orphan')

    @property  # todo if something went wrong with locations return the location_id prop and its usages
    def location(self):
        return self.duty_type.location

    @property
    def duty_roles(self):
        return [duty_role for duty_role in self.duty_type.duty_roles]

    # ------ replacements -------
    # TODO
    def replace_cadets(self, replaced_id, replacing_id):
        try:
            cadet_duty = next((cd for cd in self.cadet_duties if cd.cadet.id == replaced_id), None)
            if cadet_duty:
                cadet_duty.cadet_id = replacing_id
                db.session.add(cadet_duty)
                db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise SQLAlchemyError(f"Database error: {str(e)}")
        except Exception as e:
            raise Exception(f"Internal server error: {str(e)}")


    def create_replacement(self, type_id=3, comment="Commentary placeholder", start_date=None, end_date=None):
        ...

    # ------- methods --------
    @staticmethod
    def create_duty(date, duty_type_id, cadet_roles_ids):
        new_duty = Duty(date=date, duty_type_id=duty_type_id)
        db.session.add(new_duty)
        db.session.commit()
        # cadet_roles_ids is a list of tuples like [(34, 1), (25, 2) ...]
        for cadet_id, role_id in cadet_roles_ids:
            cadet_duty = CadetDuty(cadet_id=cadet_id, duty_id=new_duty.id, duty_role_id=role_id)
            db.session.add(cadet_duty)
        db.session.commit()

    def add_cadet(self, cadet_id):
        cadet_duty = CadetDuty.query.filter_by(cadet_id=cadet_id, duty_id=self.id).first()
        if cadet_duty:
            db.session.delete(cadet_duty)
            db.session.commit()

    def remove_cadet(self, cadet_id):
        cadet_duty = CadetDuty.query.filter_by(cadet_id=cadet_id, duty_id=self.id).first()
        if cadet_duty:
            db.session.delete(cadet_duty)
            db.session.commit()

    # ------- reserves --------
    @property
    def reserve_cadets(self):
        return [reserve_cadet_duty.cadet for reserve_cadet_duty in self.reserve_cadet_duties]

    def add_reserve_cadet(self, cadet_id, duty_role_id, priority=1):
        reserve_cadet_duty = ReserveCadetDuty(cadet_id=cadet_id, duty_role_id=duty_role_id, priority=priority)
        self.reserve_cadet_duties.append(reserve_cadet_duty)
        db.session.commit()

    # using cadet_id instead of role+priority
    def remove_reserve_cadet(self, cadet_id):
        # with db.session.no_autoflush:
        reserve_cadet_duty = next((rc for rc in self.reserve_cadet_duties if rc.cadet_id == cadet_id), None)
        if reserve_cadet_duty:
            db.session.delete(reserve_cadet_duty)
        # db.session.commit()
        print('REMOVED))')

    def free_reserves(self):
        for reserve_cadet_duty in self.reserve_cadet_duties:
            reserve_cadet_duty.delete()

    '''def fill_reserves(self):
        ...'''

    # similar to the 'reserve' prop in get_cadets_with_roles_and_reserves() method, consider removing
    def get_reserves_for_role(self, duty_role_id):
        reserves = []
        for reserve_cadet_duty in self.reserve_cadet_duties:
            if reserve_cadet_duty.duty_role_id == duty_role_id:
                reserves.append(reserve_cadet_duty.cadet)
        return sorted(reserves, key=lambda x: reserve_cadet_duty.priority)

    def get_cadets_with_roles(self):
        return [{'cadet': cadet_duty.cadet.to_dict(), 'role': cadet_duty.duty_role.to_dict()} for cadet_duty in
                self.cadet_duties]

    def get_roles_with_cadets(self):
        return [{'role': cadet_duty.duty_role.to_dict()} for cadet_duty in
                self.cadet_duties]

    def get_cadets_with_roles_and_reserves(self):
        return [
            {
                "cadet": cadet_duty.cadet.to_dict(),
                "role": cadet_duty.duty_role.to_dict(),
                "reserve": [
                    reserve_cadet_duty.to_dict() for reserve_cadet_duty in self.reserve_cadet_duties
                    if reserve_cadet_duty.duty_role_id == cadet_duty.duty_role_id
                ]
            } for cadet_duty in self.cadet_duties
        ]

    def to_dict(self):  # assume the detailed dict is used for editing a duty
        return {
            'id': self.id,
            'date': self.date.strftime('%Y-%m-%d'),
            'archived': self.archived,
            'location': self.duty_type.location.to_dict(),
            'duty_type': self.duty_type.to_dict(),
            'cadets_with_roles': self.get_cadets_with_roles_and_reserves()
        }

    def to_table_dict(self):  # a short dict for the table filling requests
        return {
            'id': self.id,
            'date': self.date.strftime('%Y-%m-%d'),
            'archived': self.archived,
            # 'roles_with_cadets': self.get_roles_with_cadets()
            'cadets_with_roles': self.get_cadets_with_roles()
        }

    def from_dict(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    UniqueConstraint('date', 'duty_type_id', name='unique_duty_type')  # can have multiple types for the same date


# общее хранилище пар наряд-курсант с ролями, большая промежуточная таблица
class CadetDuty(db.Model):
    __tablename__ = "cadet_duty"

    def __init__(self, cadet_id, duty_id, duty_role_id):
        self.cadet_id = cadet_id
        self.duty_id = duty_id
        self.duty_role_id = duty_role_id

    cadet_id = Column(Integer, ForeignKey('cadets.id'), primary_key=True)
    duty_id = Column(Integer, ForeignKey('duties.id'), primary_key=True)
    duty_role_id = Column(Integer, ForeignKey('duty_roles.id'), nullable=False)

    cadet = relationship('Cadet')
    duty = relationship('Duty', back_populates='cadet_duties')  # add this line
    duty_role = relationship('DutyRole', back_populates='cadet_duties')

    ## reserve_cadets = relationship('ReserveCadetDuty', back_populates='cadet_duty')
    # no cadet twice at the same duty
    UniqueConstraint('cadet_id', 'duty_id', name='unique_cadet_role')


# used to store all the reserve cadets for each role in each duty
# single role can have multiple reserve cadets
# each entry is a single reserve cadet
class ReserveCadetDuty(db.Model):  # todo: may replacing it with the one below will make the code cleaner
    __tablename__ = "reserve_cadet_duties"
    id = Column(Integer, primary_key=True)
    duty_id = Column(Integer, ForeignKey('duties.id'), nullable=False)
    cadet_id = Column(Integer, ForeignKey('cadets.id'), nullable=False)
    duty_role_id = Column(Integer, ForeignKey('duty_roles.id'), nullable=False)
    priority = Column(Integer, nullable=False, default=1)

    duty = relationship('Duty', back_populates='reserve_cadet_duties')
    cadet = relationship('Cadet')
    duty_role = relationship('DutyRole')

    UniqueConstraint('duty_id', 'cadet_id', 'duty_role_id', name='unique_reserve_cadet_duty')

    def to_dict(self):  # reserve cadet dict + priority
        cadet_dict = {}
        cadet_dict.update(self.cadet.to_dict())
        cadet_dict['priority'] = self.priority
        return cadet_dict

    def delete(self):
        db.session.delete(self)
        db.session.commit()


'''##class ReserveCadetDuty(db.Model):
    __tablename__ = "reserve_cadet_duties"
    id = Column(Integer, primary_key=True)
    cadet_duty_id = Column(Integer, ForeignKey('cadet_duty.cadet_id'), nullable=False)
    reserve_cadet_id = Column(Integer, ForeignKey('cadets.id'), nullable=False)
    priority = Column(Integer, nullable=False, default=1)

    cadet_duty = relationship('CadetDuty', backref='reserve_cadets')
    reserve_cadet = relationship('Cadet')

    UniqueConstraint('cadet_duty_id', 'reserve_cadet_id', name='unique_reserve_cadet_duty')'''


class Cadet(db.Model):
    __tablename__ = "cadets"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=True)
    sex = Column(Enum('M', 'F'), nullable=True)  # TODO: make nonnull

    rank_id = Column(Integer, ForeignKey('ranks.id'), nullable=False)
    position_id = Column(Integer, ForeignKey('positions.id'), nullable=False)

    pm_cell_id = Column(Integer, ForeignKey('pm_cells.id'), nullable=True)
    ak_cell_id = Column(Integer, ForeignKey('ak_cells.id'), nullable=True)

    group_id = Column(Integer, ForeignKey('groups.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    faculty_id = Column(Integer, ForeignKey('faculties.id'))
    main_location_id = Column(Integer, ForeignKey('locations.id'))

    rank = relationship('Rank')
    position = relationship('Position')
    group = relationship('Group', back_populates='cadets')
    course = relationship('Course', back_populates='cadets')
    faculty = relationship('Faculty', back_populates='cadets')
    main_location = relationship('Location')  # direct relationship

    duties = relationship('Duty', secondary='cadet_duty', back_populates='cadets')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'pm_cell_id': self.pm_cell_id,
            'faculty': self.faculty.name,
            'course': self.course_id,
            'group': self.group.name,
            'main_location': self.main_location.address
        }

    def to_dict_full(self):  # for user page
        return {
            'id': self.id,
            'name': self.name
            # TODO
        }
    # ... some columns to track statistics


class PMCells(db.Model):
    __tablename__ = 'pm_cells'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))


class AKCells(db.Model):
    __tablename__ = 'ak_cells'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))


class Rank(db.Model):
    __tablename__ = 'ranks'
    id = Column(Integer, primary_key=True)
    rank_name = Column(String(50), nullable=False)


class Position(db.Model):
    __tablename__ = 'positions'
    id = Column(Integer, primary_key=True)
    position_name = Column(String(50), nullable=False)


class Faculty(db.Model):
    __tablename__ = 'faculties'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)

    courses = relationship('Course', back_populates='faculty')
    groups = relationship('Group', back_populates='faculty')
    cadets = relationship('Cadet', back_populates='faculty')
    location = relationship('Location', back_populates='faculties')


class Course(db.Model):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)  # the id is enough
    faculty_id = Column(Integer, ForeignKey('faculties.id'), nullable=False)

    faculty = relationship('Faculty', back_populates='courses')
    groups = relationship('Group', back_populates='course')
    cadets = relationship('Cadet', back_populates='course')


class Group(db.Model):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    number_of_cadets = Column(Integer, nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'))
    faculty_id = Column(Integer, ForeignKey('faculties.id'))

    course = relationship('Course', back_populates='groups')
    faculty = relationship('Faculty', back_populates='groups')
    cadets = relationship('Cadet', back_populates='group')


'''
import random
pm_cell_range = range(1, 31)
group_ids = [1, 2, 3]
positions_per_group = {1: [4, 5, 5, 5], 2: [4, 5, 5, 5], 3: [4, 5, 5, 5]}

# Populate with 90 random cadets
for i in range(90):
    cadet = Cadet(
        name=f'RandomName{i}',
        surname=f'RandomSurname{i}',
        patronymic=f'RandomPatronymic{i}',
        rank_id=1,  # Assuming 10 ranks exist
        position_id=6,
        pm_cell_id=random.choice(pm_cell_range),
        course_id=1,
        faculty_id=1,
        main_location_id=1
    )

    group_id = random.choice(group_ids)
    cadet.group_id = group_id
    if group_id in positions_per_group:
        cadet.position_id = positions_per_group[group_id].pop(0)
    db.session.add(cadet)
db.session.commit()
'''
