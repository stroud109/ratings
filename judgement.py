from flask import Flask, render_template, redirect, request, session, url_for, flash
import datetime
import model
app = Flask(__name__)
app.secret_key = "shhhhhhhhhhhhhhsupersecretthing"

@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/", methods=["POST"])
# def sign_up():
#     pass

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
def view_all_users(): #same as index, above
    user_list = model.session.query(model.User).limit(20).all()
    return render_template("user_list.html", users = user_list)

@app.route("/users/<user_id>")
def view_user_ratings(user_id):
    user_ratings = model.session.query(model.Ratings).filter_by(user_id = user_id).all()
    return render_template("user_ratings.html", ratings = user_ratings)

@app.route("/movies")
def view_all_movies():
    movie_list = model.session.query(model.Movies).limit(100).all()
    return render_template("movies.html", movies = movie_list)

@app.route("/movies/<movie_id>")
def view_movie(movie_id): # change to display movie title, not ID
    movie_details = model.session.query(model.Ratings).filter_by(movie_id=movie_id).all()
    return render_template("movie_ratings.html", details = movie_details)

@app.route("/movies/<movie_id>", methods=["POST"])
def rate_movie(movie_id):
    print "rating movie"
    rating = request.form.get("ratingRadio")
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