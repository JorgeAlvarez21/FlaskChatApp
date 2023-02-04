from sqlalchemy import Column, String, DateTime, ForeignKey, LargeBinary, Sequence, Integer
from sqlalchemy.sql import func
from database import db_base
from uuid import uuid4


def CreateUUID():
    return uuid4().hex


class User(db_base):
    __tablename__ = "Users"

    userID = Column(String(32), unique=True, primary_key=True, default=CreateUUID)
    fullname = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    username = Column(String(200), unique=True, index=True)
    password_hash = Column(String(), nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=True)

    def __repr__(self):
        return '<User {}>'.format(User.username)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserPreferences(db_base):
    __tablename__ = "SavedUserPreferences"

    userID = Column(String(32), ForeignKey('Users.userID'), unique=True, primary_key=True)
    load_theme = Column(String, nullable=True)
    profile_picture = Column(LargeBinary, nullable=True)
    pinned_messages = Column(String, nullable=True)
    display_status = Column(String(30), nullable=True)


class UserAlerts(db_base):
    __tablename__ = "UserAlerts"
    alertID = Column(String(32), unique=True, primary_key=True, default=CreateUUID)
    to_userID = Column(String(32), ForeignKey('Users.userID'), nullable=False, index=True)
    from_userID = Column(String(32), ForeignKey('Users.userID'), nullable=False, index=True)
    from_username = Column(String(32), nullable=False, index=True)
    type = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    message = Column(String(200), nullable=False)
    sub_message = Column(String(200), nullable=False)
    action_label = Column(String(200), nullable=False)
    status = Column(String(20), nullable=False)
    response = Column(String(20), nullable=False)
    notify_receiver = Column(String(10), default='false')
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # __table_args__ = (UniqueConstraint('alertID', name='uq_alertID'))

class Contacts(db_base):
    __tablename__ = "Contacts"
    contactID = Column(String(32), unique=True, primary_key=True, default=CreateUUID)
    userID = Column(String(32), ForeignKey('Users.userID'))
    contact_userID = Column(String(32), nullable=False)
    groupID = Column(String(32), default=CreateUUID)
    contact_since = Column(DateTime(timezone=True), server_default=func.now())
    friendship_status = Column(String(20), default='pending')
    # __table_args__ = (UniqueConstraint('contactID', name='uq_contact'))


class Inbox(db_base):
    __tablename__ = "InboxCollection"
    msgID = Column(String, default=CreateUUID, nullable=False, primary_key=True)
    groupID = Column(String(32), nullable=False)
    userID_one = Column(String(32))
    userID_two = Column(String(32))
    sent_by_one = Column(String(10), nullable=True, default=None)
    msg_content = Column(String(300), nullable=True, default=None)
    timestamp_sent = Column(DateTime(timezone=True), server_default=func.now())
    # __table_args__ = (UniqueConstraint('groupID', 'group_creatorID', name='uq_groupID'))

# class CreatedChatGroups(db_base):
#     __tablename__ = "ChatGroups"
#     groupID = Column(String(32), unique=True, primary_key=True)
#     group_name = Column(String(32), nullable=False)
#     group_size = Column(Integer)
#     group_members = Column(String, nullable=False, index=True)

# __table_args__ = (UniqueConstraint('groupID', 'group_creatorID', name='uq_groupID'))

# class UserChatGroups(db_base):
#     __tablename__ = "UserChatGroups"
#     groupID_userID = Column(String(32), unique=True, primary_key=True)
#     groupID = Column(String(32), ForeignKey('ChatGroups.groupID'))
#     userID = Column(String(32), ForeignKey('Users.userID'))
#
#     __table_args__ = (UniqueConstraint('contactID', name='uq_contact'))
