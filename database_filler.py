from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Post

engine = create_engine('sqlite:///data.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# generic user
user = User(name='Bob', password_hash='temp_hash')
session.add(user)
session.commit()

post = Post(user_id=1, title='Why cats are better than dogs', content='Cats are better than dogs because cats are cuter than dogs.')
session.add(post)

post = Post(user_id=1, title='I have something important to admit...', content='I like pineapple on my pizza.')
session.add(post)

post = Post(user_id=1, title='DAE literally do the thing that everyone does?', content='I do this everyday and I feel so weird doing it but it\'s nice to know that I\'m not alone in doing it I guess I\'m not that weird.')
session.add(post)

session.commit()