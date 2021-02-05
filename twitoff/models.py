"""SQLAlchemy models and utility fucntions for TwitOff"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

# User table with columns id and name
class User(DB.Model):  #  inherits DB.Model here
  """Twitter Users corresponding to Tweets"""
  id = DB.Column(DB.BigInteger, primary_key=True)
  name = DB.Column(DB.String, nullable=False)
  newest_tweet_id = DB.Column(DB.BigInteger)

  def __repr__(self):
    return "<User: {}>".format(self.name)


# Tweet table with columns id, text, and user_id
class Tweet(DB.Model):
  """Tweet related to a user"""
  #  Primary id column
  id = DB.Column(DB.BigInteger, primary_key=True)
  #  text column of character length 300 (unicode)
  text = DB.Column(DB.Unicode(300))
  vect = DB.Column(DB.PickleType, nullable=False)
  #  Foreign Key = user.id
  user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
  user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))  # like a join on User but not a join
  # references the text from class Tweet that references the User


  def __repr__(self):
    return "<Tweet: {}>".format(self.text)
