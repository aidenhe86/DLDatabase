"""Models for Duel Links card database"""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User in the system."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.Text, nullable = False, unique = True)

    password = db.Column(db.Text, nullable = False)

    decks = db.relationship("Deck", backref="user")

    @classmethod
    def signup(cls, username, password):
        """Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Deck(db.Model):
    """User Deck in the system"""

    __tablename__ = "decks"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id",ondelete="cascade"),
                        primary_key=True)

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )
    
    # maindeck
    md1_id = db.Column(db.Integer, nullable=False)
    md2_id = db.Column(db.Integer, nullable=False)
    md3_id = db.Column(db.Integer, nullable=False)
    md4_id = db.Column(db.Integer, nullable=False)
    md5_id = db.Column(db.Integer, nullable=False)
    md6_id = db.Column(db.Integer, nullable=False)
    md7_id = db.Column(db.Integer, nullable=False)
    md8_id = db.Column(db.Integer, nullable=False)
    md9_id = db.Column(db.Integer, nullable=False)
    md10_id = db.Column(db.Integer, nullable=False)
    md11_id = db.Column(db.Integer, nullable=False)
    md12_id = db.Column(db.Integer, nullable=False)
    md13_id = db.Column(db.Integer, nullable=False)
    md14_id = db.Column(db.Integer, nullable=False)
    md15_id = db.Column(db.Integer, nullable=False)
    md16_id = db.Column(db.Integer, nullable=False)
    md17_id = db.Column(db.Integer, nullable=False)
    md18_id = db.Column(db.Integer, nullable=False)
    md19_id = db.Column(db.Integer, nullable=False)
    md20_id = db.Column(db.Integer, nullable=False)

    md21_id = db.Column(db.Integer)
    md22_id = db.Column(db.Integer)
    md23_id = db.Column(db.Integer)
    md24_id = db.Column(db.Integer)
    md25_id = db.Column(db.Integer)
    md26_id = db.Column(db.Integer)
    md27_id = db.Column(db.Integer)
    md28_id = db.Column(db.Integer)
    md29_id = db.Column(db.Integer)
    md30_id = db.Column(db.Integer)

    # extra deck
    ed1_id = db.Column(db.Integer)
    ed2_id = db.Column(db.Integer)
    ed3_id = db.Column(db.Integer)
    ed4_id = db.Column(db.Integer)
    ed5_id = db.Column(db.Integer)
    ed6_id = db.Column(db.Integer)
    ed7_id = db.Column(db.Integer)

class Like(db.Model):
    """Mapping user likes on decks"""

    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id", ondelete="cascade"))

    deck_id = db.Column(db.Integer,
                        db.ForeignKey("decks.id",ondelete="cascade"))






