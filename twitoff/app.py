"""Main app/routing file for Twitoff"""

"""Flask command code just below"""
"""
export FLASK_APP=app.py
flask run

export FLASK_APP=twitoff (main directory)
flask shell (gives a REPL to run Flask in python)
"""


from flask import Flask, render_template, request  #1
from .models import DB, User
from .twitter import add_or_update_user, update_all_users
from os import getenv  # imports .env file
from .predict import predict_user


def create_app():
    """Creates and Configures a Flask application"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URI")  #  getenv("DATABASE_URI")  
    app.config['SQLALCHEMY_TRACK_MODICATIONS'] = False   # if I make changes I don't need to know about it
    DB.init_app(app)   #  initialize the DataBase with the application

    @app.route('/')  # This is the base url (@app.route- specific to Flask) `Listens for the page request/visit` 
    def root():
        # SELECT * from User table;
        # users = User.query.all()   # creating a query and running all of the User table in models.py
        return render_template("base.html", title="Home", users=User.query.all()) # at this point create a base.html template

    @app.route('/compare', methods=['POST'])
    def compare():
        # grabs inputted values from the dropdown 
        user0, user1 = sorted(
            [request.values['user1'],
            request.values['user2']]
        )

        if user0 == user1:
            message = "Cannot compare the same user"

        else:
            prediction = predict_user(user0, user1, request.values['tweet_text'])
            message = "{} is more likely to be said by {} than {}".format(
                request.values['tweet_text'], user1 if prediction else user0,
                user0 if prediction else user1)

        return render_template('prediction.html', title='Prediction', message=message)

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        # either grab a user that already exist in our DB or grab the users input
        name = name or request.values['user_name']

        try:
            # if button is clicked then do this
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User {} sucessfully added!'.format(name)
            # tweets are always collected if the user exist
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            # if we get an error then no tweets are displayed
            tweets=[]

        return render_template('user.html', title=name, tweets=tweets, message=message)
    # @app.route("/about")
    # def about():
    #     return "About me"

    # @app.route("/projects")
    # def projects():
    #     return "Portfolio - Projects"

  
    @app.route('/update')
    def update():
        # reset()     # check
        # insert_example_users()  # check
        # updates our users from the function in twitter.py
        update_all_users()
        return render_template('base.html', title="Tweets have been updated!", users=User.query.all())

    @app.route('/reset')
    def reset():
        # resets database
        DB.drop_all()
        # creates database again
        DB.create_all()
        return render_template('base.html', title='Reset Database!')


    return app

    #  TODO - make the rest of application
# def create_app(): #1
#     """ Creates and Configures a Flask application"""
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URI")
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     DB.init_app(app)


#     @app.route('/')
#     def root():
#         DB.drop_all()
#         DB.create_all()

#         users = User.query.all()
#         return render_template("base.html", title="Home", users=users)


#     @app.route('/compare', methods=['POST'])
#     def compare():
#         # grabs inputted values from the dropdown 
#         user0, user1 = sorted(
#             [request.values['user1'],
#              request.values['user2']]
#         )

#         if user0 == user1:
#             # tells application user they cant compare same twitter users
#             message = "Cannot compare users to themselves!"

#         else:
#             # running prediction and return the prediction to user as a message
#             prediction = predict_user(user0, user1, request.values['tweet_text'])
#             message = "{} is more likely to be said by {} than {}".format(
#                 request.values['tweet_text'], user1 if prediction else user0,
#                 user0 if prediction else user1)

#         return render_template('prediction.html', title='Prediction', message=message)


#     @app.route('/user', methods=['POST'])
#     @app.route('/user/<name>', methods=['GET'])
#     def user(name=None, message=''):
#         # either grab a user that already exist in our DB or grab the users input
#         name = name or request.values['user_name']

#         try:
#             # if button is clicked then do this
#             if request.method == 'POST':
#                 add_or_update_user(name)
#                 message = 'User {} sucessfully added!'.format(name)
#             # tweets are always collected if the user exist
#             tweets = User.query.filter(User.name == name).one().tweets
#         except Exception as e:
#             message = "Error adding {}: {}".format(name, e)
#             # if we get an error then no tweets are displayed
#             tweets=[]

#         return render_template('user.html', title=name, tweets=tweets, message=message)


#     @app.route('/update')
#     def update():
#         reset()     # check
#         insert_temp_users()  # check
#         # updates our users from the function in twitter.py
#         update_all_users()
#         return render_template('base.html', title="Tweets have been updated!", users=User.query.all())


#     @app.route('/reset')
#     def reset():
#         # resets database
#         DB.drop_all()
#         # creates database again
#         DB.create_all()
#         return render_template('base.html', title='Reset Database!')


#     def insert_temp_users():
#         get_user('nasa')
#         get_user('elonmusk')

    # return app