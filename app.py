from flask import Flask, request, render_template
from flask_migrate import Migrate

import config
from views.posts import post_app
from models.database import db

app = Flask(__name__)
app.register_blueprint(post_app, url_prefix="/posts")

app.config.update(
    SQLALCHEMY_DATABASE_URI=config.SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db.init_app(app)
Migrate(app, db, compare_type=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return "Hello POST!!"
    name = request.args.get("name") or "World"
    return render_template("index.html", name=name)

@app.cli.command('init-db', with_appcontext=True)
def initialize_db():
    """
    Create initial db
    # not use due to Flask-Migrate
    """
    print("Do init db")
    db.create_all()
    print("init db done")

if __name__ == "__main__":
    app.run(
        host="localhost",
        port=5000,
        debug=True
    )
