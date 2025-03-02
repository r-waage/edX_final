import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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

    """Show portfolio of stocks"""
    #Define a list of stocks for the logged in user to loop over
    id_usr = session["user_id"]
    stock_rows = db.execute(
        "SELECT DISTINCT stock FROM buy_sell_stocks WHERE user_id = ?", id_usr
    )

    list_dict_stocks = []
    grand_total = 0
    #Loop through the list of stocks
    for stocks in stock_rows:
        #set the stock's symbol
        stock_symbol = stocks["stock"]

        #lookup the price of this stock
        stock_info = lookup(stock_symbol)
        stock_curr_price = float(stock_info["price"])

        #Quantity of Shares owned
        #quantity_stock = db.execute(
            #"SELECT sum(quantity) as quantity FROM buy_sell_stocks WHERE user_id = ? AND stock = ?", id_usr, stock_symbol
        #)
        #quant_stock = float(quantity_stock[0]["quantity"])

        #########################################################

        #Check how many shares of the stock are available
        rows = db.execute(
            "SELECT action, sum(quantity) as quant FROM buy_sell_stocks WHERE stock = ? AND user_id = ? GROUP BY action", stock_symbol, id_usr
        )

        #check that rows only include 2 rows max one for buy and one for sell
        # Ensure username exists and password is correct
        if len(rows) > 2:
            return apology("invalid return of number of rows during index action", 403)

        #loop through the rows and store the buy and sell quantities
        buy_quantity = 0
        sell_quantity = 0
        available_quantity = 0
        for row in rows:
            if row["action"] == "buy":
                buy_quantity = row["quant"]
            elif row["action"] == "sell":
                sell_quantity = row["quant"]

        available_quantity = float(buy_quantity - sell_quantity)

        #########################################################

        #Total value of stock holdings
        total_stock_holding = stock_curr_price * available_quantity
        grand_total = grand_total + total_stock_holding


        #Build dictionary
        #dict = {'Stock':stock_info["symbol"], 'Quantity':quant_stock, 'Curr_Price':usd(stock_curr_price), 'Total_Value':usd(total_stock_holding)}
        if total_stock_holding >= 0:
            dict = {'Stock':stock_info["symbol"], 'Quantity':available_quantity, 'Curr_Price':usd(stock_curr_price), 'Total_Value':usd(total_stock_holding)}

        #Append dictionary to the list
        list_dict_stocks.append(dict)

    #set the users cash
    amount_cash = db.execute(
        "SELECT cash FROM users WHERE id = ?", id_usr
    )
    usr_cash = float(amount_cash[0]["cash"])
    grand_total = grand_total + usr_cash

    return render_template("index.html", list = list_dict_stocks, cash=usd(usr_cash), grand=usd(grand_total) )

    #return render_template("quoted.html", Stock = stock_info["name"], Price = stock_info["price"], Symbol=stock_info["symbol"])



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    stock_info = {}
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("Enter a stock symbol", 400)
        else:
            stock_info = lookup(request.form.get("symbol"))
            #try:
                #stock_info = lookup(request.form.get("symbol"))
            #except Exception as e:
                #print(f"An error occurred, while calling a stock quote: {e}")
            #return apology("Error during Stock Quote call", 403)

        if stock_info == None:
            return apology("Stock Symbol doesn't exist",400)
        else:
            return render_template("quoted.html", Stock = stock_info["name"], Price = usd(stock_info["price"]), Symbol=stock_info["symbol"])

    else:

        return render_template("quote.html")


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
            "INSERT INTO  users (username, hash) VALUES(?,?)", request.form.get("username"), generate_password_hash(request.form.get("password"))
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
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    stock_list = []
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        #Render an apology if the input is not a positive integer
        if not request.form.get("shares"):
            return apology("Enter Quantity of Shares you want to sell", 403)
        else:
            form_quantity = float(request.form.get("shares"))

        if int(form_quantity) < 0:
            return apology("Only positive number of shares can be sold", 403)

        #store Info from sell.html
        form_symbol = request.form.get("symbol")

        #store the user_id
        id_usr = session["user_id"]

        #Check how many shares of the stock are available
        rows = db.execute(
            "SELECT action, sum(quantity) as quant FROM buy_sell_stocks WHERE stock = ? AND user_id = ? GROUP BY action", form_symbol, id_usr
        )

        #check that rows only include 2 rows max one for buy and one for sell
        # Ensure username exists and password is correct
        if len(rows) > 2:
            return apology("invalid return of number of rows during sell action", 403)

        #loop through the rows and store the buy and sell quantities
        buy_quantity = 0
        sell_quantity = 0
        for row in rows:
            if row["action"] == "buy":
                buy_quantity = row["quant"]
            elif row["action"] == "sell":
                sell_quantity = row["quant"]

        available_quantity = float(buy_quantity - sell_quantity)

        #get current price of the stock
        stock_info = lookup(request.form.get("symbol"))

        if stock_info == None:
            return apology("Stock Symbol doesn't exist",403)

        stock_price = float(stock_info["price"])

        #insert sell of stock if enough shares are available
        if available_quantity >= form_quantity:
            #save sell to the database
            try:
                id = db.execute(
                    "INSERT INTO buy_sell_stocks (user_id, action, stock, price, quantity, date) VALUES (?,?,?,?,?,?)", id_usr, "sell", form_symbol, stock_price, form_quantity, datetime.now()
                )
            except Exception as e:
                print(f"An error occurred, when inserting the sell transaction: {e}")
                return apology("Something went wrong, while inserting the buy transaction",403)
        else:
            return apology("The quantity of stocks is not available",403)


        #Update the users cash - first get the cash
        # Query database for username
        try:
            cash = db.execute(
                "SELECT cash FROM users WHERE id = ?", id_usr
                )
        except Exception as e:
            print(f"An error occurred, when selecting cash from user: {e}")
            return apology("Something went wrong, when selecting cash from user",403)

        sum_price_quantity = stock_price * form_quantity

        #Calculate the new value, add to cash as stocks are sold
        new_value = float(cash[0]["cash"]) + sum_price_quantity

        try:
            id = db.execute(
                "UPDATE users SET cash = ? WHERE id = ?", new_value, id_usr
            )
        except Exception as e:
            print(f"An error occurred, when inserting the buy transaction: {e}")
            return apology("Something went wrong, while inserting the buy transaction",403)

        # Redirect user to home page
        return redirect("/")

    else:
        #Populate the SELECT list in html
        id_usr = session["user_id"]
        stock_rows = db.execute(
        "SELECT DISTINCT stock FROM buy_sell_stocks WHERE user_id = ? AND action = 'buy'", id_usr
        )

        for item in stock_rows:
            stock_list.append(item["stock"])

        return render_template("sell.html", list = stock_list)



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("Enter a stock symbol", 400)
        else:
            stock_info = lookup(request.form.get("symbol"))
            #try:
                #stock_info = lookup(request.form.get("symbol"))
            #except Exception as e:
                #print(f"An error occurred, while calling a stock quote: {e}")
            #return apology("Error during Stock Quote call", 403)

        if stock_info == None:
            return apology("Stock Symbol doesn't exist",400)
        elif not request.form.get("shares"):
            return apology("Enter Quantity of Shares you want to buy", 400)
        else:
            quantity = request.form.get("shares")

        print(f"Quantity: {quantity}")

        if int(quantity) < 0:
            return apology("Only positive number of shares can be bought", 400)

        #Lookup a stocks current price
        stock_price = stock_info["price"]
        print(f"stockprice: {stock_price}")

        #SELECT how much cash the user currently has in users
        id_usr = session["user_id"]
        amount_cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", id_usr
        )

        #print(f"Amount Cash: {amount_cash[0]["cash"]}")

        #Render an apology if the user cannot afford the number of shares at the current price
        price_stock = float(stock_price)
        quantity_stock = float(quantity)
        sum_price_quantity = price_stock * quantity_stock
        if sum_price_quantity > float(amount_cash[0]["cash"]):
            return apology("You can not afford the number of shares", 400)
        else:
            try:
                id = db.execute(
                    "INSERT INTO buy_sell_stocks (user_id, action, stock, price, quantity, date) VALUES (?,?,?,?,?,?)", id_usr, "buy", stock_info["symbol"], usd(price_stock), quantity_stock, datetime.now()
                )
            except Exception as e:
                print(f"An error occurred, when inserting the buy transaction: {e}")
                return apology("Something went wrong, while inserting the buy transaction",400)

        #Update the users cash - first get the cash
        # Query database for username
        try:
            cash = db.execute(
                "SELECT cash FROM users WHERE id = ?", id_usr
                )
        except Exception as e:
            print(f"An error occurred, when selecting cash from user: {e}")
            return apology("Something went wrong, when selecting cash from user",400)

        #Calculate the new value
        new_value = float(cash[0]["cash"]) - sum_price_quantity

        try:
            id = db.execute(
                "UPDATE users SET cash = ? WHERE id = ?", new_value, id_usr
            )
        except Exception as e:
            print(f"An error occurred, when inserting the buy transaction: {e}")
            return apology("Something went wrong, while inserting the buy transaction",400)

        # Redirect user to home page
        return redirect("/")

            #return render_template("quoted.html", Stock = stock_info["name"], Price = stock_info["price"], Symbol=stock_info["symbol"])
    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    #Define a list of transactions for the logged in user to loop over
    id_usr = session["user_id"]
    try:
         trans_rows = db.execute(
         #"SELECT DISTINCT stock FROM buy_sell_stocks WHERE user_id = ?", id_usr
         "SELECT action, Stock, price, quantity, date FROM buy_sell_stocks WHERE user_id =? ORDER BY date", id_usr
         )
         print(trans_rows)
    except sqlite3.Error as e:
        print(f"history: an error occured during select: {e}")
        apology("history: an error occured during select ",403)

    return render_template("history.html", list = trans_rows)


@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():

    if request.method == "POST":

        #Get additional cash amount
        if not request.form.get("cash_amount"):
            return apology("Enter Cash Amount", 403)
        else:
            cash_amount = request.form.get("cash_amount")

        #check if the cash_amount is numeric
        if not cash_amount.isnumeric():
            return apology("Enter a numeric value", 403)

        if float(cash_amount) < 0:
            return apology("cash Amount needs to be positive", 403)


        # Query database for cash of logged in user
        id_usr = session["user_id"]
        try:
            cash = db.execute(
                "SELECT cash FROM users WHERE id = ?", id_usr
                )
        except Exception as e:
            print(f"An error occurred, when selecting cash from user: {e}")
            return apology("Something went wrong, when selecting cash from user",403)

        #Calculate the new value
        new_cash = float(cash[0]["cash"]) + float(cash_amount)

        try:
            id = db.execute(
                "UPDATE users SET cash = ? WHERE id = ?", new_cash, id_usr
            )
        except Exception as e:
            print(f"An error occurred, when inserting cash: {e}")
            return apology("Something went wrong, while inserting the buy transaction",403)

        # Redirect user to home page
        return redirect("/")

    else:

        return render_template("cash.html")


