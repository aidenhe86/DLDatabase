"""Duel Links card database application"""

import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

CURR_USER_KEY = "curr_user"

from forms import UserAddForm,LoginForm
from models import db, connect_db, User, Deck, Like
from cards import request_card

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///duellinks'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

db.create_all()

##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route("/signup",methods=["GET","POST"])
def signup():
    """Handle user signup"""

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("Logout Successfully!", "success")

    return redirect("/")

##############################################################################
#  User Route
@app.route("/users/<int:user_id>")
def users_show(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)

    # snagging messages in order from the database;
    # user.messages won't be in order by default
    # messages = (Message
    #             .query
    #             .filter(Message.user_id == user_id)
    #             .order_by(Message.timestamp.desc())
    #             .limit(100)
    #             .all())

    if g.user:
        likes = [msg.id for msg in g.user.likes]
    else:
        likes = []
    return render_template('users/show.html', user=user, likes=likes)



##############################################################################
#  Search card
@app.route("/card_search")
def searchcard():
    """search card"""
    card = {}

    # card name
    name = request.args.get("fname")
    if name:
        card["name"] = name

    # spell/trap card
    ctype = request.args.get("ctype")
    if ctype == "Spell Card" or ctype == "Trap Card":
        card["type"] = ctype

    #monster card
    elif ctype == "Monster" or ctype == "Extra Monster":
        # monster type
        mtype = request.args.get("mtype")
        if mtype != "Monster Type":
            card["type"] = mtype
        else:
            flash("Please select Monster Type.", "danger")
            return redirect("/card_search")

        # pendulum monster scale
        if "Pendulum" in mtype:
            scale = request.args.get("scale")
            if scale != "Scale":
                card["scale"] = scale
        
        # monster attribute
        attr = request.args.get("attr")
        if attr != "Attribute":
            card["attribute"] = attr

        # monster level
        lv = request.args.get("lv")
        if lv != "Level":
            card["level"] = lv

        # monster attack
        atkNum = request.args["atkNum"]
        if atkNum:
            atkSymbol = request.args.get("atkSymbol")
            card["atk"] = atkSymbol + atkNum
        
        # monster defense
        defNum = request.args.get("defNum")
        if defNum:
            defSymbol = request.args.get("defSymbol")
            card["def"] = defSymbol + defNum

    # card race
    race = request.args.get("race")
    if race:
        if race != "Card Race":
            card["race"] = race

    print("********************")
    print(card)
    print("********************")

    cards = request_card(card)
    
    if cards == []:
        flash("No card matching! Please try again.", "danger")
    return render_template("cards/cards.html",cards=cards)

##############################################################################
# Decks
@app.route("/decks")
def listdeck():
    decks = Deck.query.all()

    return render_template("decks/show.html",decks=decks)

# @app.route("/decks/add")
# def adddeck():




##############################################################################
# Homepage
@app.route("/")
def homepage():
    """Show homepage"""

    return render_template("home.html")