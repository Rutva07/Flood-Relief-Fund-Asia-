import csv
import os

from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
from datetime import datetime


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/")
@login_required
def index():
    return render_template("index.html")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        if not firstname:
            error_text = "Please enter First name"
            return render_template("apology.html", error_text=error_text)
        lastname = request.form.get("lastname")
        if not lastname:
            error_text = "Please enter Last name"
            return render_template("apology.html", error_text=error_text)
        username = request.form.get("username")
        if not username:
            error_text = "Please enter Username"
            return render_template("apology.html", error_text=error_text)
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password:
            error_text = "Please enter password"
            return render_template("apology.html", error_text=error_text)
        if not confirmation:
            error_text = "Please enter confirmation password"
            return render_template("apology.html", error_text=error_text)
        if (confirmation != password):
            error_text = "Password and its confirmation should match"
            return render_template("apology.html", error_text=error_text)

        user = db.execute("SELECT * FROM users WHERE username=?", username)
        if user:
            error_text = "PLease choose different username"
            return render_template("apology.html", error_text=error_text)

        db.execute("INSERT INTO users (firstname, lastname, username, password) VALUES(?, ?, ?, ?)", firstname, lastname, username, password)
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            error_text = "Must provide username"
            return render_template("apology.html", error_text=error_text)

        elif not request.form.get("password"):
            error_text = "Must provide password"
            return render_template("apology.html", error_text=error_text)

        rows = db.execute("SELECT * FROM users WHERE username = ? AND password = ?", request.form.get("username"), request.form.get("password"))
        if len(rows) != 1:
            error_text = "Username or Password is wrong"
            return render_template("apology.html", error_text=error_text)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/amount")
@login_required
def amount():
    available = db.execute("SELECT * FROM available")
    fund = available[0]["fund"]
    return render_template("totalfund.html", fund = fund)


@app.route("/donorlist")
@login_required
def donorlist():
    donors = db.execute("SELECT SUM(amount) AS total_amount, person_id FROM donors GROUP BY person_id ORDER BY total_amount DESC")
    return render_template("donorlist.html", donors=donors)


@app.route("/donate", methods=["GET", "POST"])
@login_required
def donate():
    if request.method == "POST":
        amount_str = request.form.get("amount")
        card_str = request.form.get("card")
        if not amount_str:
            error_text = "Please enter valid Amount"
            return render_template("apology.html", error_text=error_text)
        amount = int(amount_str)
        if amount <= 0:
            error_text = "Please enter valid Amount"
            return render_template("apology.html", error_text=error_text)
        if not card_str:
            error_text = "Please enter card details"
            return render_template("apology.html", error_text=error_text)
        card = int(card_str)
        digit = 0
        i = card
        net = 0
        found = False

        while i > 0:
            i = int(i / 10)
            digit = digit + 1

        if (digit == 16):
            k = card
            while (k > 100):
                k = int(k / 10)
            if ((k == 51) or (k == 52) or (k == 53) or (k == 54) or (k == 55)):
                found = True
            else:
                net = net + 1
        else:
            net = net + 1

        if ((digit == 13) or (digit == 16)):
            m = card
            while (m > 10):
                m = int(m / 10)
            if (m == 4):
                n = card
                sum = 0
                n = int(n / 10)
                y = 0
                while (n > 0):
                    y = (n % 10) * 2
                    while (y > 0):
                        sum = sum + y % 10
                        y = int(y / 10)
                    n = int(n / 100)
                x = card
                while (x > 0):
                    sum = sum + (x % 10)
                    x = int(x / 100)
                if (sum % 10 == 0):
                    found = True
                else:
                    net = net + 1
            else:
                net = net + 1
        else:
            net = net + 1

        if net == 2:
             error_text = "Please enter valid card number"
             return render_template("apology.html", error_text=error_text)

        person_id = session["user_id"]
        current_datetime = datetime.now()
        db.execute("INSERT INTO donors (person_id, date, amount) VALUES(?, ?, ?)", person_id, current_datetime, amount)

        available = db.execute("SELECT * FROM available")
        fund = available[0]["fund"]
        db.execute("UPDATE available SET fund = ?", fund + amount)

        return redirect("/")

    else:
        return render_template("donate.html")


@app.route("/require", methods=["GET", "POST"])
@login_required
def require():
    if request.method == "POST":
        amount_str = request.form.get("amount")
        if not amount_str:
            error_text = "Please enter proper withdraw amount"
            return render_template("apology.html", error_text=error_text)
        amount = int(amount_str)
        if amount <= 0 or amount > 500:
            error_text = "Please enter proper withdraw amount"
            return render_template("apology.html", error_text=error_text)

        country = request.form.get("country")
        if not country:
            error_text = "Please enter country name"
            return render_template("apology.html", error_text=error_text)

        data_list = []

        # Open the CSV file and read its data into a list of dictionaries
        with open('flood.csv', mode='r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if row["Disaster Type"] == "Flood":
                    data_list.append(row)

        country_lower = country.lower()
        found = False
        for element in data_list:
            if element["Country"].lower() == country_lower:
                found = True

        if found == False:
            error_text = country + " is not affected by flood"
            return render_template("apology.html", error_text=error_text)

        passport_number = request.form.get("passport_number")
        length = len(passport_number)

        country_lower = country.lower()
        if country_lower == "india" or country_lower == "malaysia":
            if length != 12:
                error_text = "Passport number of " + country + " is not valid"
                return render_template("apology.html", error_text=error_text)
        else:
            if length != 9:
                error_text = "Passport number of " + country + " is not valid"
                return render_template("apology.html", error_text=error_text)

        available = db.execute("SELECT * FROM available")
        fund = available[0]["fund"]
        if amount > fund:
            error_text = "There is not enough fund available"
            return render_template("apology.html", error_text=error_text)

        db.execute("UPDATE available SET fund = ?", fund - amount)

        person_id = session["user_id"]
        current_datetime = datetime.now()
        db.execute("INSERT INTO receivers (person_id, date, amount, passport_number) VALUES(?, ?, ?, ?)", person_id, current_datetime, amount, passport_number)
        return redirect("/")

    else:
        return render_template("require.html")