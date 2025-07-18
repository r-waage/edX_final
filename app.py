import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology

app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route('/')
def first_page():
	return render_template("FirstPage_ETF.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Ensure password confirmation matches
        elif not (request.form.get("password") == request.form.get("confirmation")):
            return apology("password confirmation doesn't match", 400)

        # Query database for username

        try:
            id = db.execute(
            #"SELECT * FROM users WHERE username = ?", request.form.get("username")
            "INSERT INTO  users (username, risk_type, hash) VALUES(?,?,?)", request.form.get("username"), request.form.get("risk_type"), generate_password_hash(request.form.get("password"))
            )
        except Exception as e:
            print(f"An error occurred, when inserting username and password: {e}")
            return apology("Duplicate username", 400)


        # Ensure username exists and password is correct
        #if len(rows) != 1 or not check_password_hash(
            #rows[0]["hash"], request.form.get("password")
        #):
            #return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        #session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register_ETF.html")


@app.route("/register_averse", methods=["GET", "POST"])
def register_averse():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Ensure password confirmation matches
        elif not (request.form.get("password") == request.form.get("confirmation")):
            return apology("password confirmation doesn't match", 400)

        # Query database for username

        try:
            id = db.execute(
            #"SELECT * FROM users WHERE username = ?", request.form.get("username")
            "INSERT INTO  users (username, risk_type, hash) VALUES(?,?,?)", request.form.get("username"), "risk_averse", generate_password_hash(request.form.get("password"))
            )
        except Exception as e:
            print(f"An error occurred, when inserting username and password: {e}")
            return apology("Duplicate username", 400)


        # Ensure username exists and password is correct
        #if len(rows) != 1 or not check_password_hash(
            #rows[0]["hash"], request.form.get("password")
        #):
            #return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        #session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register_ETF_averse.html")


@app.route("/register_balanced", methods=["GET", "POST"])
def register_balanced():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Ensure password confirmation matches
        elif not (request.form.get("password") == request.form.get("confirmation")):
            return apology("password confirmation doesn't match", 400)

        # Query database for username

        try:
            id = db.execute(
            #"SELECT * FROM users WHERE username = ?", request.form.get("username")
            "INSERT INTO  users (username, risk_type, hash) VALUES(?,?,?)", request.form.get("username"), "balanced", generate_password_hash(request.form.get("password"))
            )
        except Exception as e:
            print(f"An error occurred, when inserting username and password: {e}")
            return apology("Duplicate username", 400)


        # Ensure username exists and password is correct
        #if len(rows) != 1 or not check_password_hash(
            #rows[0]["hash"], request.form.get("password")
        #):
            #return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        #session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register_ETF_balanced.html")


@app.route("/register_seeking", methods=["GET", "POST"])
def register_seeking():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Ensure password confirmation matches
        elif not (request.form.get("password") == request.form.get("confirmation")):
            return apology("password confirmation doesn't match", 400)

        # Query database for username

        try:
            id = db.execute(
            #"SELECT * FROM users WHERE username = ?", request.form.get("username")
            "INSERT INTO  users (username, risk_type, hash) VALUES(?,?,?)", request.form.get("username"), "risk_seeking", generate_password_hash(request.form.get("password"))
            )
        except Exception as e:
            print(f"An error occurred, when inserting username and password: {e}")
            return apology("Duplicate username", 400)


        # Ensure username exists and password is correct
        #if len(rows) != 1 or not check_password_hash(
            #rows[0]["hash"], request.form.get("password")
        #):
            #return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        #session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register_ETF_seeking.html")

#if __name__ == '__main__':
	#app.run(host='0.0.0.0', port=5000)