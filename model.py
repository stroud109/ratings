from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import correlation

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

    def similarity(self, other):
        u_ratings = {}
        paired_ratings = []
        for r in self.ratings:
            u_ratings[r.movie_id] = r

        for r in other.ratings:
            u_r = u_ratings.get(r.movie_id)
            if u_r:
                paired_ratings.append((u_r.rating, r.rating))

        if paired_ratings:
            # print paired_ratings
            return correlation.pearson(paired_ratings)

        else:
            return 0.0

    def rating_prediction(self, movie):
        other_ratings = movie.ratings
        similarities = [ (self.similarity(rating.user), rating) for rating in other_ratings ]
        similarities.sort(reverse=True)
        pos_sim = [ s for s in similarities if s[0] > 0]
        if not pos_sim:
            return None
        numerator = sum([r.rating * similarity for similarity, r in pos_sim])
        denominator = sum([similarity[0] for similarity in pos_sim])
        print numerator, denominator
        print numerator/denominator
        return numerator/denominator

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



    # users = []
    # for other_u in other_users:
    #     similarity = user.similarity(other_u)
    #     pair = (similarity, other_u)
    #     users.append(pair)
    # sorted_users = sorted(users, reverse = True)
    # top_user = sorted_users[0]

    # top_user_rating = session.query(Ratings).filter_by(user_id = top_user[1].id, movie_id = movie.id).one()
    # top_user_rating = top_user_rating.rating
    # predicted_rating = top_user[0] * top_user_rating
    # return predicted_rating

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
