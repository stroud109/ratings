from flask import Flask, render_template, redirect, request, session, url_for, flash
import model
app = Flask(__name__)
app.secret_key = "shhhhhhhhhhhhhhsupersecretthing"

@app.route("/")
def index():
    user_list = model.session.query(model.User).limit(10).all()
    print "rendered template"
    return render_template("user_list.html", users = user_list)

# @app.route("/", methods=["POST"])
# def sign_up():
#     pass

@app.route("/", methods=["POST"])
def sign_in():
    print "signing in!"
    email = request.form.get("email")
    password = request.form.get("password")
    print email, password
    user_id = model.authenticate(email, password)
    if user_id != None:
        flash("loggedin!")

        session['user_id'] = user_id
        # return redirect(url_for("view_user_ratings", user_id = user_id))
    else:
        flash("Password or email incorrect. Try again.")
    return redirect(url_for("index"))

@app.route("/users")
def view_all_users():
    pass

@app.route("/users/<user_id>")
def view_user_ratings():
    pass

@app.route("/movies")
def view_all_movies():
    pass

@app.route("/movies/<name>")
def view_movie():
    pass

@app.route("/movies/<name>", methods=["POST"])
def rate_movie():
    pass

@app.route("/clear")
def session_clear():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug = True)