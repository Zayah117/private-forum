import sys
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(String(80), nullable=False)
	picture = Column(String(250))

class Post(Base):
	__tablename__ = 'post'

	id = Column(Integer, primary_key=True)
	title = Column(String(length=80), nullable=False)
	content = Column(String(length=1000), nullable=False)
	user = relationship(User)
	user_id = Column(Integer, ForeignKey('user.id'))

engine = create_engine('sqlite:///data.db')

Base.metadata.create_all(engine)