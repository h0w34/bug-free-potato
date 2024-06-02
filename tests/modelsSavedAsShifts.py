from sqlalchemy import Column, Boolean
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date

from app import db


class Location(db.Model):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    faculties = relationship('Faculty', back_populates='location')


class Position(db.Model):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    shift_type_id = Column(Integer, ForeignKey('shift_types.id'), nullable=False)  # each shift belongs to a shiftType

    shift_type = relationship('ShiftType', back_populates='positions')
    cadet_shifts = relationship('CadetShift', back_populates='position')


class ShiftType(db.Model):
    __tablename__ = "shift_types"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    positions = relationship('Position', back_populates='shift_type')  # one shift can have multiple positions
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    description = Column(String(200))

    location = relationship('Location')


class Shift(db.Model):
    __tablename__ = "duties"
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    shift_type_id = Column(Integer, ForeignKey('shift_types.id'), nullable=False)
    archived = Column(Boolean, default=False)

    shift_type = relationship('ShiftType')
    cadets = relationship('Cadet', secondary='cadet_shifts', back_populates='duties')

    @property
    def location(self):
        return self.shift_type.location

    @property
    def positions(self):
        return [cadet_shift.position for cadet_shift in self.cadet_shifts]


# общее хранилище пар наряд-курсант, промежуточная таблица
class CadetShift(db.Model):
    __tablename__ = "cadet_shifts"
    cadet_id = Column(Integer, ForeignKey('cadets.id'), primary_key=True)
    shift_id = Column(Integer, ForeignKey('duties.id'), primary_key=True)
    position_id = Column(Integer, ForeignKey('positions.id'), nullable=False)

    position = relationship('Position', back_populates='cadet_shifts')

    # no cadet twice at the same shift
    UniqueConstraint('cadet_id', 'shift_id', name='unique_cadet_shift_position')


class Cadet(db.Model):
    __tablename__ = "cadets"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=True)
    rank_id = Column(Integer, ForeignKey('ranks.id'), nullable=False)
    pm_cell_id = Column(Integer, ForeignKey('pm_cells.id', name='fk_cadet_pm_cell'), nullable=True)
    ak_cell_id = Column(Integer, ForeignKey('ak_cells.id', name='fk_cadet_ak_cell'), nullable=True)

    group_id = Column(Integer, ForeignKey('groups.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    faculty_id = Column(Integer, ForeignKey('faculties.id'))
    main_location_id = Column(Integer, ForeignKey('locations.id', name='fk_cadet_locations'))

    rank = relationship()
    group = relationship('Group', back_populates='cadets')
    course = relationship('Course', back_populates='cadets')
    faculty = relationship('Faculty', back_populates='cadets')
    main_location = relationship('Location')  # direct relationship

    # viewonly is for not to overlap FKeys
    shifts = relationship('Shift', secondary='cadet_shifts', back_populates='cadets')

    # some columns to track statistics


class PMCells(db.Model):
    __tablename__ = 'pm_cells'
    id = Column(Integer, primary_key=True, unique=True)
    location_id = Column(Integer, ForeignKey('locations.id'))


class AKCells(db.Model):
    __tablename__ = 'ak_cells'
    id = Column(Integer, primary_key=True, unique=True)
    location_id = Column(Integer, ForeignKey('locations.id'))


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

