"""Main app/routing logic for Twitoff"""

from os import getenv
from flask import Flask, render_template, request
from .twitter import add_or_update_user, update_all_users
from .models import DB, User
from .predict import predict_user
from dotenv import load_dotenv 


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")  #"sqlite:///db.sqlite3"
    # app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)


    @app.route('/')
    def root():
        # SQL equivalent = "SELECT * FROM user;"
        return render_template('base.html', title="Home", users=User.query.all())

    
    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template("base.html", title="Reset Database")

    
    @app.route("/update")
    def update():
        users = User.query.all()
        for user in users:
            add_or_update_user(user.name)
        return render_template("base.html", title="Database has been updated!", users=User.query.all())


    @app.route("/user", methods=["POST"])
    @app.route("/user/<name>", methods=["GET"])
    def user(name=None, message=""):
        name = name or request.values["user_name"]
        try:
            if request.method == "POST":
                add_or_update_user(name)
                message = "User {} sucessfully added!".format(name)

            tweets = User.query.filter(User.name == name).one().tweets

        except Exception as e:
            message = "Error handling {}: {}".format(name, e)
            tweets = []

        return render_template("user.html", title=name, tweets=tweets, message=message)


    @app.route("/compare", methods=["POST"])
    def compare():
        user0, user1 = sorted(
            [request.values["user1"], request.values["user2"]])

        # conditinoal that prevents same user comparison
        if user0 == user1:
            message = "Cannot compare users to themselves!"

        else:
            hypo_tweet_text = request.values["tweet_text"]
            # prediction return zero or one depending upon user
            prediction = predict_user(user0, user1, hypo_tweet_text)
            message = "'{}' is more likely to be said by {} than {}".format(
                hypo_tweet_text, user1 if prediction else user0,
                user0 if prediction else user1
            )

        # returns rendered template with dynamic message
        return render_template('prediction.html', title="Prediction:", message=message)

    return app






# """Main app/routing file for Twitoff"""

# """Flask command code just below"""
# """
# export FLASK_APP=app.py
# flask run

# export FLASK_APP=twitoff (main directory)
# flask shell (gives a REPL to run Flask in python)
# """

# from flask import Flask, render_template, request  # request allows posting
# from .models import DB, User
# from .twitter import add_or_update_user   #, update_all_users, insert_example_users
# from os import getenv  # imports .env file
# from .predict import predict_user


# def create_app():
#     """Creates and Configures a Flask application"""
#     app = Flask(__name__)

#     app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URI")  #  getenv("DATABASE_URI")  
#     app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
#     # app.config['SQLALCHEMY_TRACK_MODICATIONS'] = False   # if I make changes I don't need to know about it
#     DB.init_app(app)   #  initialize the DataBase with the application

#     @app.route('/')  # This is the base url (@app.route- specific to Flask) `Listens for the page request/visit` 
#     def root():
#         # SELECT * FROM user;
#         # users = User.query.all()   # creating a query and running all of the User table in models.py
#         return render_template(
#             "base.html", 
#             title="Home", 
#             users=User.query.all()) # at this point create a base.html template

#     @app.route('/compare', methods=["POST"])
#     def compare():
#         # grabs inputed values from the dropdown 
#         user0, user1 = sorted(
#             [request.values['user1'], request.values['user2']]
#             )

#         if user0 == user1:
#             message = "Cannot compare the same user"

#         else:
#             hypo_tweet_text = request.values["tweet_text"]
#             #  Prediction returns 0 or 1 based on the user...0 or 1
#             prediction = predict_user(user0, user1, hypo_tweet_text)
#             message = "'{}' is more likely to be said by {} than {}".format(
#                 hypo_tweet_text, user1 if prediction else user0,
#                 user0 if prediction else user1
#                 )

#         return render_template(
#             'prediction.html', 
#             title='Prediction', 
#             message=message)

#     @app.route("/user", methods=["POST"])
#     @app.route("/user/<name>", methods=["GET"])
#     def user(name=None, message=""):
#         # either grab a user that already exist in" our DB or grab the users input
#         name = name or request.values["user_name"]

#         try:
#             # if button is clicked then do this
#             if request.method == "POST":
#                 add_or_update_user(name)
#                 message = "User {} sucessfully added!".format(name)
#             # tweets are always collected if the user exist
#             tweets = User.query.filter(User.name == name).one().tweets

#         except Exception as e:
#             message = "Error adding {}: {}".format(name, e)
#             # if we get an error then no tweets are displayed
#             tweets=[]

#         return render_template(
#             'user.html', 
#             title=name, 
#             tweets=tweets, 
#             message=message)

#     # @app.route("/about")
#     # def about():
#     #     return "About me"

#     # @app.route("/projects")
#     # def projects():
#     #     return "Portfolio - Projects"

  
#     @app.route("/update")
#     def update():
#         users = User.query.all()
#         for user in users:
#             add_or_update_user(user.name)
#         # updates our users from the function in twitter.py
#         return render_template(
#             'base.html', 
#             title="Tweets have been updated!", 
#             users=User.query.all())

#     @app.route("/reset")
#     def reset():
#         # resets database
#         DB.drop_all()
#         # creates database again
#         DB.create_all()
#         return render_template(
#             'base.html', 
#             title='Reset Database!')


#     return app