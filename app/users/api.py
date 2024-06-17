from flask_restful import Resource, Api, reqparse, abort
from sqlalchemy import func

from app.users.models import User
from app.duties.models import Cadet, Duty
from datetime import datetime, timedelta, date


class UserResource(Resource):
    def get(self, username):
        user = User.get_by_username(username)
        if not user:
            print(f'NO USER! {username}')
            abort(404, message=f'User {username} doesnt exist')

        print(user)
        return {'user': user.to_dict(), 'cadet': user.cadet.to_dict()}


# or CadetStatistics?
class UserStatisticsResource(Resource):
    def get(self, username):
        '''parser = reqparse.RequestParser()
        parser.add_argument('start_date', type=str, required=True)
        parser.add_argument('end_date', type=str, required=True)
        args = parser.parse_args()'''
        user: User = User.get_by_username(username)
        cadet: Cadet = user.cadet
        if user is None:
            abort(404, message=f'User {username} does not exist')
        if cadet is None:
            abort(404, message=f'User {username} has no linked cadet')

        curr_month_start_date = datetime.now().replace(day=1)
        curr_month_end_date = (curr_month_start_date.replace(day=28) + timedelta(days=4)).replace(
            day=1) - timedelta(days=1)
        current_year = datetime.now().year
        curr_year_start_date = date(current_year, 1, 1)
        curr_year_end_date = date(current_year, 12, 31)

        return {
            'stats': {
                'current_month': self.calculate_statistics(cadet, curr_month_start_date, curr_month_end_date),
                'current_year': self.calculate_statistics(cadet, curr_year_start_date, curr_year_end_date)
            },
            'future_duties':
                [{'duty': duty.to_dict(), 'role': duty.get_role_by_cadet_id(cadet.id).to_dict()}
                 for duty in cadet.future_duties]
            ,
            'future_reserves':
                [reserve.to_dict() for reserve in cadet.future_reserves]

        }

    # let the frontend deside what period to fetch
    # the response contains the cadet/user stats with the schedule info (planned duties etc.)
    @staticmethod
    def calculate_statistics(cadet, start_date, end_date):
        duties_count = cadet.duties.filter(Duty.date >= start_date, Duty.date <= end_date).count()
        weekend_duties_count = cadet.duties.filter(func.extract('dow', Duty.date) >= 5).count()
        replaced_count = cadet.replaced_by_date_count(start_date, end_date)
        was_replaced_count = cadet.was_replaced_by_date_count(start_date, end_date)

        return {
            'duties_count': duties_count,
            'weekend_duties_count': weekend_duties_count,
            'replaced_count': replaced_count,
            'was_replaced_count': was_replaced_count
            # some additional stats in future
        }


class CadetStatisticsService:
    def __init__(self, session):
        self.session = session

    def calculate_statistics(self, start_date, end_date):
        # Calculate statistics for the given date range

        pass

    def get_statistics(self, year=None, month=None):
        if year and month:
            # Get statistics for a specific month and year
            pass
        elif year:
            # Get statistics for a specific year
            pass
        else:
            # Get all statistics
            pass
