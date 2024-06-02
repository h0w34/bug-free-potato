from sqlalchemy import Column, Boolean
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date
from sqlalchemy.ext.hybrid import hybrid_property

from app import db


class Location(db.Model):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    faculties = relationship('Faculty', back_populates='location')

    duty_types = relationship('DutyType')

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


class DutyType(db.Model):
    __tablename__ = "duty_types"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    duty_roles = relationship('DutyRole', back_populates='duty_type')  # one duty can have multiple duty_roles
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    description = Column(String(250))

    location = relationship('Location')

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
    archived = Column(Boolean, default=False)

    duty_type = relationship('DutyType')
    # cadets = association_proxy('cadet_duties', 'cadet')
    cadets = relationship('Cadet', secondary='cadet_duty', back_populates='duties')
    cadet_duties = relationship('CadetDuty', back_populates='duty')

    @property
    def location(self):
        return self.duty_type.location

    @property
    def location_id(self):
        return self.location.id

    @property
    def duty_roles(self):
        return [duty_role for duty_role in self.duty_type.duty_roles]

    @hybrid_property  # remove hybrid?
    def cadets_with_roles(self):
        return [(cadet_duty.cadet, cadet_duty.duty_role) for cadet_duty in self.cadet_duties]

    def get_cadets_with_roles(self):
        return [(cadet_duty.cadet.to_dict(), cadet_duty.duty_role.to_dict()) for cadet_duty in self.cadet_duties]

    def get_cadets_by_roles(self):
        return

    @staticmethod
    def create_duty(date, duty_type_id, cadet_roles_ids):
        new_duty = Duty(date=date, duty_type_id=duty_type_id)
        db.session.add(new_duty)
        db.session.commit()

        for cadet_id, role_id in cadet_roles_ids:
            cadet_duty = CadetDuty(cadet_id=cadet_id, duty=new_duty, duty_role_id=role_id)
            db.session.add(cadet_duty)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.strftime('%Y-%m-%d'),
            'archived': self.archived,
            'location': self.duty_type.location.to_dict(),
            'duty_type': self.duty_type.to_dict(),
            'cadets_with_roles': self.get_cadets_with_roles()
        }

    def to_table_dict(self):
        return{
            'id': self.id,
            'date': self.date.strftime('%Y-%m-%d'),
            'archived': self.archived,
            'cadets_with_roles': self.get_cadets_with_roles()
        }

    def from_dict(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    UniqueConstraint('date', 'duty_type_id', name='unique_duty_type')  # can have multiple types for the same date


# общее хранилище пар наряд-курсант, промежуточная таблица
class CadetDuty(db.Model):
    __tablename__ = "cadet_duty"
    cadet_id = Column(Integer, ForeignKey('cadets.id'), primary_key=True)
    duty_id = Column(Integer, ForeignKey('duties.id'), primary_key=True)
    duty_role_id = Column(Integer, ForeignKey('duty_roles.id'), nullable=False)

    cadet = relationship('Cadet')
    duty = relationship('Duty', back_populates='cadet_duties')  # add this line
    duty_role = relationship('DutyRole', back_populates='cadet_duties')

    # no cadet twice at the same duty
    UniqueConstraint('cadet_id', 'duty_id', name='unique_cadet_role')


class Cadet(db.Model):
    __tablename__ = "cadets"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=True)

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

    def to_dict_full(self):
        return {
            'id': self.id,
            'name': self.name
            # TODO
        }

    # some columns to track statistics


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