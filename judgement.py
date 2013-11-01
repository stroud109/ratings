from flask import Flask, render_template, redirect, request, session, url_for, flash
import datetime, random
import model
app = Flask(__name__)
app.secret_key = "shhhhhhhhhhhhhhsupersecretthing"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    search_term = request.args.get("search")
    search_results = model.session.query(model.Movies).filter(model.Movies.name.like("%"+search_term+"%"))
    return render_template('search.html', search_results = search_results, search_term = search_term)

@app.route("/", methods=["POST"])
def sign_in():
    email = request.form.get("email")
    password = request.form.get("password")
    user_id = model.authenticate(email, password)
    if user_id != None:
        flash("loggedin!")

        session['user_id'] = user_id
        print session.get('user_id')
        # return redirect(url_for("view_user_ratings", user_id = user_id))
    else:
        flash("Password or email incorrect. Try again.")
    return redirect(url_for("index"))

@app.route("/users")
def view_all_users():
    user_list = model.session.query(model.User).limit(20).all()
    return render_template("user_list.html", users = user_list)

@app.route("/users/<user_id>")
def view_user_ratings(user_id):
    user_ratings = model.session.query(model.Ratings).filter_by(user_id = user_id).all()
    return render_template("user_ratings.html", ratings = user_ratings)

@app.route("/movies")
def view_all_movies():
    random_start = random.randint(0, 1500)
    random_end = random_start + 100
    movie_list = model.session.query(model.Movies).filter(model.Movies.id > random_start, model.Movies.id < random_end).all()
    return render_template("movies.html", movies = movie_list)

@app.route("/movies/<movie_id>")
def view_movie(movie_id):
    movie_details = model.session.query(model.Ratings).filter_by(movie_id=movie_id).all()
    movie = model.session.query(model.Movies).filter_by(id = movie_id).one()
    user_id = session.get('user_id')
    the_eye = model.session.query(model.User).filter_by(id=946).one()
    prediction = None
    eye_rating = None
    if user_id:
        rating = model.session.query(model.Ratings).filter_by(movie_id = movie_id, user_id = user_id).all()
        if not rating:
            user = model.session.query(model.User).filter_by(id = user_id).one()
            prediction = user.rating_prediction(movie)
            effective_rating = prediction

            eye_rating = model.session.query(model.Ratings).filter_by(user_id = the_eye.id, movie_id = movie.id).first()
        else:
            effective_rating = rating[0].rating

        if not eye_rating:
            eye_rating = the_eye.rating_prediction(movie)
        else:
            eye_rating = eye_rating.rating

        difference = abs(eye_rating - effective_rating)

        messages = [ "I suppose you don't have such bad taste after all.",
             "I regret every decision that I've ever made that has brought me to listen to your opinion.",
             "Words fail me, as your taste in movies has clearly failed you.",
             "That movie is great. For a clown to watch. Idiot.",]

        beratement = messages[int(difference)]

    return render_template("movie_ratings.html", details = movie_details, rating = rating, prediction = prediction, beratement = beratement)

@app.route("/movies/<movie_id>", methods=["POST"])
def rate_movie(movie_id):
    print "rating movie"
    rating = request.form.get("ratingRadio")
    if rating:
        new_rating = model.Ratings(movie_id = movie_id, user_id = session.get("user_id"), timestamp = datetime.datetime.now(), rating = rating)
        model.add_rating(new_rating) #add + commit

        flash("Your rating has been recorded!")
    return redirect(url_for("view_movie", movie_id = movie_id))


@app.route("/clear")
def session_clear():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug = True)
