from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

engine = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User(Base): # child
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)
    age = Column(Integer, nullable = True)
    zipcode = Column(String(15), nullable = True)

class Movies(Base): # parent
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable = True)
    released_at = Column(Date(), nullable = True)    
    #DD-Mon-YYYY
    imdb_url = Column(String(300), nullable = True)

class Ratings(Base): # association
    __tablename__ = "ratings"
    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer(), ForeignKey('movies.id'), nullable = True)
    user_id = Column(Integer(), ForeignKey('users.id'), nullable = True)
    timestamp = Column(DateTime(), nullable = True)
    #unix seconds since 1/1/1970
    rating = Column(Integer(), nullable = True)

    user = relationship("User",
                        backref=backref("ratings", order_by=id))
    movies = relationship("Movies", 
                        backref=backref("ratings", order_by=id))


### End class declarations

def authenticate(in_email, in_password):
    in_password = hash(in_password)
    user = session.query(User).filter_by(email = in_email, password = in_password).first()
    if user != None:
        return user.id
    else:
        return None

def add_rating(new_rating):
    session.add(new_rating)
    session.commit()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
