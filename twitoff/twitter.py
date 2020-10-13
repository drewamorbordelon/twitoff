"""Retrieve Tweets, word embeddings, and populate DB"""
import tweepy
import spacy
from .models import DB, Tweet, User


TWITTER_API_KEY = 'tfw9TiPzSmPdVTkSowgAPPY5D'
TWITTER_API_KEY_SECRET = 'uQw9MgqT6eLWO3imL3sKSsD8klAtF5qfLxHDtwVE5r1mnp1ALE'
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)


# Create a function to grab a USER twitter handle
def add_or_update_user(username):
    """Allows to add/update users to our database"""
    twitter_user = TWITTER.get_user(username)
    db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.ide, name=username)
    DB.session.add(db_user)

    tweets = twitter_user.timeline(
        count=200, exclude_replies=True,
        include_rts=False, tweet_mode='extended'
    )

    for tweet in tweets:
        db_tweet = Tweet(id=tweet.id, text=tweet.full_text)
        db_user.tweets.append(db_tweet)
        DB.session.add(db_tweet)

    DB.session.commit()
