from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__='user'

    id = Column(Integer,primary_key=True, autoincrement=True)
    name = Column(String)
    favorites = relationship('Favorite', backref='user', lazy='subquery')

        # Definindo um construtor para aceitar `name`
    def __init__(self, name):
        self.name = name



class Favorite(Base):
    __tablename__ = 'favorite'

    id = Column(Integer,primary_key=True, autoincrement=True)
    symbol = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, symbol, user_id):
        self.symbol = symbol
        self.user_id = user_id

