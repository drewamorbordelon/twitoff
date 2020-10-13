"""Main app/routing file for TwitOff"""

from flask import Flask, render_template
from .models import DB, User, insert_example_users


def create_app():
    """Create and configure an instance of the Flask application"""

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3" # where DB is stored
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    DB.init_app(app)

    # ... TODO make the app
    @app.route('/')  # Decorator = extend and modify behavior of a class, method, function
    def root():
        insert_example_users()  #  calls function within models.py - insert users
        return render_template("base.html", title="Home", users=User.query.all())

    # when you run the application we haven't built any other
    # functionality other than the users showing up so keep that in mind    
    @app.route('/update')
    def update():
        #  Reset the database 
        DB.drop_all()  #  Deletes already present databases
        DB.create_all()  #  Creates the database from scratch
        insert_example_users()
        return render_template('base.html', title="Users updated!", users=User.query.all())

    return app



    

    # """This is the Static form"""
    # from flask import Flask

    # def create_app():
    #     """Create an configure an instance of the Flask application"""
    #     app = Flask(__name__)

    #     @app.route('/')
    #     def root():
    #         return "Hello!"

    #     return app