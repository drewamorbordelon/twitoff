"""SQLAlchemy models and utility functions for Twitoff"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    """Tweets corresponding to Twitter Users"""

    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)

    def __repr__(self):
        return "- User {} -".format(self.name)

class Tweet(DB.Model):
    """Tweet text and data for a user"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))

    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship("User", backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return "- Tweet {} -".format(self.text)

#  Example users but remember they don't have tweets
def insert_example_users():
    """Example Users"""
    bill = User(id=1, name="BillGates")
    elon = User(id=2, name="ElonMusK")

    DB.session.add(bill)
    DB.session.add(elon)
    DB.session.commit()
