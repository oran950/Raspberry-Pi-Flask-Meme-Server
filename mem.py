from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
import json

app = Flask(__name__)

# Configure SQLAlchemy to use Google Cloud SQL for MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:paswword@0.0.0.0:3306/name_of_db'
# 0.0.0.0 localhost portsql:3306  
db = SQLAlchemy(app)

#  the data model
class Meme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meme_url = db.Column(db.String(200))
    subreddit = db.Column(db.String(50))

with app.app_context():
    db.create_all()

# Function to get a meme from an API
def get_meme():
    url = "https://meme-api.com/gimme"
    response = json.loads(requests.get(url).text)
    meme_url = response["preview"][-1]  
    subreddit = response["subreddit"]
    return meme_url, subreddit

# Route to insert a meme into the database and display it
@app.route("/")
def index():
    meme_url, subreddit = get_meme()
    meme = Meme(meme_url=meme_url, subreddit=subreddit)
    db.session.add(meme)
    db.session.commit()
    return render_template("inedx_meme.html", meme_url=meme_url, subreddit=subreddit)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
