"""Duel Links card database application"""

import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from datetime import datetime

CURR_USER_KEY = "curr_user"

from forms import UserAddForm,LoginForm
from models import db, connect_db, User, Deck
from cards import request_card

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///duellinks'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
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
#  API route
# Search card
@app.route("/api/card_search")
def searchcard():
    """search card and return json"""
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
            return jsonify(error="Please select Monster Type.")

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
        
    # send card to ext API and return response
    cards = request_card(card)

    return jsonify(cards)

##############################################################################
# Page

# Homepage
@app.route("/")
def homepage():
    """Show homepage"""
    decks = Deck.query.order_by(Deck.timestamp.desc()).limit(20).all()

    return render_template("home.html",decks=decks)

# Cards
@app.route("/search")
def search():
    """card search page and return search result"""

    return render_template("cards/cards.html")

# Decks
@app.route("/decks")
def listdeck():
    """list all users shared deck"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    decks = Deck.query.filter(Deck.user_id == g.user.id).order_by(Deck.timestamp.desc()).limit(20).all()

    return render_template("decks/list.html",decks=decks)

@app.route("/decks/add",methods=["GET","POST"])
def newdeck():
    """add new deck"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if request.method == "POST":
        newDeck = Deck(
            user_id = g.user.id,
            name = request.json["name"],

            md1_id = request.json["md1_id"],
            md2_id = request.json["md2_id"],
            md3_id = request.json["md3_id"],
            md4_id = request.json["md4_id"],
            md5_id = request.json["md5_id"],
            md6_id = request.json["md6_id"],
            md7_id = request.json["md7_id"],
            md8_id = request.json["md8_id"],
            md9_id = request.json["md9_id"],
            md10_id = request.json["md10_id"],
            md11_id = request.json["md11_id"],
            md12_id = request.json["md12_id"],
            md13_id = request.json["md13_id"],
            md14_id = request.json["md14_id"],
            md15_id = request.json["md15_id"],
            md16_id = request.json["md16_id"],
            md17_id = request.json["md17_id"],
            md18_id = request.json["md18_id"],
            md19_id = request.json["md19_id"],
            md20_id = request.json["md20_id"],

            md21_id = request.json.get("md21_id"),
            md22_id = request.json.get("md22_id"),
            md23_id = request.json.get("md23_id"),
            md24_id = request.json.get("md24_id"),
            md25_id = request.json.get("md25_id"),
            md26_id = request.json.get("md26_id"),
            md27_id = request.json.get("md27_id"),
            md28_id = request.json.get("md28_id"),
            md29_id = request.json.get("md29_id"),
            md30_id = request.json.get("md30_id"),

            ed1_id = request.json.get("ed1_id"),
            ed2_id = request.json.get("ed2_id"),
            ed3_id = request.json.get("ed3_id"),
            ed4_id = request.json.get("ed4_id"),
            ed5_id = request.json.get("ed5_id"),
            ed6_id = request.json.get("ed6_id"),
            ed7_id = request.json.get("ed7_id")
        )
        db.session.add(newDeck)
        db.session.commit()

        return "",204

    else:
        return render_template("decks/adddeck.html")

@app.route("/decks/<int:deck_id>")
def showdeck(deck_id):
    """show all current user deck"""

    deck = Deck.query.get_or_404(deck_id)
    return render_template("decks/show.html",deck=deck)


@app.route("/decks/<int:deck_id>/edit",methods=["GET","POST"])
def editdeck(deck_id):
    """edit exist user deck"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    deck = Deck.query.get_or_404(deck_id)

    if request.method == "POST":
        deck.name = request.json["name"],
        deck.timestamp = datetime.utcnow(),
        deck.md1_id = request.json["md1_id"],
        deck.md2_id = request.json["md2_id"],
        deck.md3_id = request.json["md3_id"],
        deck.md4_id = request.json["md4_id"],
        deck.md5_id = request.json["md5_id"],
        deck.md6_id = request.json["md6_id"],
        deck.md7_id = request.json["md7_id"],
        deck.md8_id = request.json["md8_id"],
        deck.md9_id = request.json["md9_id"],
        deck.md10_id = request.json["md10_id"],
        deck.md11_id = request.json["md11_id"],
        deck.md12_id = request.json["md12_id"],
        deck.md13_id = request.json["md13_id"],
        deck.md14_id = request.json["md14_id"],
        deck.md15_id = request.json["md15_id"],
        deck.md16_id = request.json["md16_id"],
        deck.md17_id = request.json["md17_id"],
        deck.md18_id = request.json["md18_id"],
        deck.md19_id = request.json["md19_id"],
        deck.md20_id = request.json["md20_id"],

        deck.md21_id = request.json.get("md21_id"),
        deck.md22_id = request.json.get("md22_id"),
        deck.md23_id = request.json.get("md23_id"),
        deck.md24_id = request.json.get("md24_id"),
        deck.md25_id = request.json.get("md25_id"),
        deck.md26_id = request.json.get("md26_id"),
        deck.md27_id = request.json.get("md27_id"),
        deck.md28_id = request.json.get("md28_id"),
        deck.md29_id = request.json.get("md29_id"),
        deck.md30_id = request.json.get("md30_id"),
        deck.ed1_id = request.json.get("ed1_id"),
        deck.ed2_id = request.json.get("ed2_id"),
        deck.ed3_id = request.json.get("ed3_id"),
        deck.ed4_id = request.json.get("ed4_id"),
        deck.ed5_id = request.json.get("ed5_id"),
        deck.ed6_id = request.json.get("ed6_id"),
        deck.ed7_id = request.json.get("ed7_id")
    
        db.session.commit()

        return "",204

    else:
        return render_template("decks/editdeck.html",deck=deck)


@app.route("/decks/<int:deck_id>/delete",methods=["POST"])
def deletedeck(deck_id):
    """delete user's deck"""
    deck = Deck.query.get_or_404(deck_id)
    if not g.user or g.user.id != deck.user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    db.session.delete(deck)
    db.session.commit()

    return redirect("/decks")