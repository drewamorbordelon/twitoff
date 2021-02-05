## Twitoff-mvp
An app that tries to predict which twitter user may have said a specific tweet

## Use for Application
The user inputs two Twitter handles. Then the application user inputs a phrase or tweet and the logistic regression algorithm attempts to predict which of the two Twitter users may have said the inputted tweet.

## Installation

Download the repo and navigate there from the command line:

```sh
git clone https://github.com/drewamorbordelon/twitoff.git
cd twitoff
```


## Setup and activate a virtual environment:

```sh
pipenv install Flask Flask-SQLAlchemy Flask Migrate
pipenv shell
```


## Running the web application - commands:

```sh  
FLASK Documentation: https://flask.palletsprojects.com/en/1.1.x/

Windows:
export FLASK_APP=twitoff
flask run

Mac:
Running the application has a slightly different command than Windows. See the documentation for FLASK.
```
