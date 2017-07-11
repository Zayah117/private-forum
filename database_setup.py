import sys
import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(String(80), nullable=False)
	password_hash = Column(String(250), nullable=False)
	picture = Column(String(250))

class Post(Base):
	__tablename__ = 'post'

	id = Column(Integer, primary_key=True)
	title = Column(String(80), nullable=False)
	content = Column(String(1000), nullable=False)
	user = relationship(User)
	user_id = Column(Integer, ForeignKey('user.id'))
	created_date = Column(DateTime, default=datetime.datetime.utcnow)

engine = create_engine('sqlite:///data.db')

Base.metadata.create_all(engine)