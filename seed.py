import model
import csv
import re
import datetime

def load_users(session):
    # use u.user

    with open("seed_data/u.user", 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter="|")
        for row in csvreader:
            id = row[0]      
            age = row[1]
            zipcode = row[4]
            new_user = model.User(id = id, age= age, zipcode = zipcode)
            session.add(new_user)

def load_movies(session):
    date_pattern = re.compile('\s[(][0-9]{4}[)]')
    with open("seed_data/u.item", 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter = "|")
        for row in csvreader:
            id = row[0]
            title = row[1]
            title = title.decode("latin-1")
            name = date_pattern.sub('', title)
            if len(row[2]) > 0:
                released_at = datetime.datetime.strptime(row[2], "%d-%b-%Y") #needs to be parsed as date
            else:
                released_at = None
            imdb_url = row[4] 
            new_movie = model.Movies(id = id, name = name, released_at = released_at, imdb_url = imdb_url)
            session.add(new_movie)

def load_ratings(session):
    # use u.data
    with open("seed_data/u.data", 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter = "\t")
        for row in csvreader:
            user_id = row[0]
            movie_id = row[1]
            rating = row[2]
            if len(row[3]) > 0:
                timestamp = datetime.datetime.fromtimestamp(float(row[3]))
            else:
                timestamp = None
            new_rating = model.Ratings(user_id = user_id, movie_id = movie_id, rating = rating, timestamp = timestamp)
            session.add(new_rating)

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_movies(session)
    load_ratings(session)
    session.commit()

if __name__ == "__main__":
    s= model.connect()
    main(s)
