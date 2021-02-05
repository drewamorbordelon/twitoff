"""Prediction of Users based on tweet embeddings"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, hypo_tweet_text):
    """
    Determine and return which user is more likely to say a given tweet

    Example run: predict_user('jackblack', 'hillaryclinton', 'I like politics and democrats')
    Return 0 (user0_name) or 1 (user1_name)
    """

    #  Grabs users from our database
    user0 = User.query.filter(User.name==user0_name).one()
    user1 = User.query.filter(User.name==user1_name).one()

    #  Grabs vectors from each tweet in user.tweets
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    #  Vertically stacking (combining vectors) to train model (x)
    vects = np.vstack([user0_vects, user1_vects])

    #  Genereate labels for the vects array (y)
    labels = np.concatenate(
      [np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])

    #  Train model and instantiate
    log_reg = LogisticRegression().fit(vects, labels)

    #  Using NLP model to generate embeddings - vectorize_tweet() - and reshapes
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text).reshape(1, -1)

    #  Predicts and returns 0 or 1 depeneding upon Logistic Regression models and prediction
    return log_reg.predict(hypo_tweet_vect)

