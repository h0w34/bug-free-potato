from app import db
from uuid import uuid4, UUID as pyUUID
from sqlalchemy.types import Date, DateTime, UUID
from datetime import datetime
from sqlalchemy.orm import relationship
import app


class RefreshSession(db.Model):
    __tablename__ = 'refresh_sessions'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='cascade'), nullable=False)
    user = relationship('User', back_populates='refresh_sessions')

    refresh_token_jti = db.Column(UUID(as_uuid=True), nullable=False)
    ua = db.Column(db.String(200), nullable=True)
    fingerprint = db.Column(db.String(200), nullable=True)
    ip = db.Column(db.String(15), nullable=True)
    expires_in = db.Column(db.Integer, nullable=False)
    created_at = db.Column(DateTime(), nullable=False, default=datetime.now())

    @classmethod
    def create_for_user(cls, user, jti, ua, fprint, ip):
        refresh_session = RefreshSession(id=uuid4())
        refresh_session.user = user
        refresh_session.refresh_token_jti = pyUUID(jti)
        refresh_session.ua = ua
        refresh_session.fingerprint = fprint
        refresh_session.ip = ip
        refresh_session.expires_in = app.Config.JWT_REFRESH_TOKEN_EXPIRES
        refresh_session.created_at = datetime.now()
        db.session.add(refresh_session)
        db.session.commit()

    def __repr__(self):
        return f'RefreshSession(id={self.id}, user_id={self.user_id}, ' \
               f'refresh_token={self.refresh_token_jti}, ua={self.ua}, fingerprint={self.fingerprint}, ' \
               f'ip={self.ip}, expires_in={self.expires_in}, created_at={self.created_at})'


    '''id = (primary_key=True, default=uuid4, editable=False)

    user_id = db.Column\
        .ForeignKey(User, related_name="sessions", db_index=True, on_delete=models.CASCADE)
    token = models.CharField(max_length=128, unique=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "sessions"'''

    '''@classmethod
    def create_for_user(cls, user):
        return Session.objects.create(
            user=user,
            token=random_string(length=32),
            created_at=datetime.utcnow(),
            expires_at=max(user.membership_expires_at, datetime.utcnow() + timedelta(days=30)),
        )'''
