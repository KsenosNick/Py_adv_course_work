
import sqlalchemy as sq
# from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from database.db_config import db_user, db_password, host_name, port, db_name

Base = declarative_base()

DSN = f'postgresql+psycopg2://{db_user}:{db_password}@{host_name}:{port}/{db_name}'

engine = sq.create_engine(DSN)
Session = sessionmaker(bind=engine)


class VKUser(Base):
    __tablename__ = 'vkuser'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, nullable=False, unique=True)
    first_name = sq.Column(sq.VARCHAR(50), nullable=False)
    last_name = sq.Column(sq.VARCHAR(50), nullable=False)
    age = sq.Column(sq.Integer)
    age_difference = sq.Column(sq.Integer)
    city = sq.Column(sq.Integer)
    sex = sq.Column(sq.Integer)
    relation = sq.Column(sq.Integer)
    common_count = sq.Column(sq.Integer)
    black_list = sq.Column(sq.Boolean)
    photos = relationship("Photo")

    def __str__(self):
        string = f'{self.user_id} {self.first_name} {self.last_name}'
        return string


class Photo(Base):
    __tablename__ = 'photo'

    id = sq.Column(sq.Integer, primary_key=True)
    photo_id = sq.Column(sq.Integer, nullable=False)
    url = sq.Column(sq.String, nullable=False)
    likes_count = sq.Column(sq.Integer)
    comments_count = sq.Column(sq.Integer)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('vkuser.id'), nullable=False)

    def __str__(self):
        return self.photo_id

