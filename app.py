from werkzeug.exceptions import NotFound
from flask import Blueprint, render_template

post_app = Blueprint("post_app", __name__)

POSTS = {
    1: "post1",
    2: "post2",
    3: "post3",
    4: "post4",
    5: "post5"
}

@post_app.route("/", endpoint="posts_list")
def posts_list():
    return render_template("posts/posts_list.html", products=POSTS)

@post_app.route("/<int:post_id>/", endpoint="posts_detail")
def post_detail(post_id):
    try:
        post_name = POSTS[post_id]
    except KeyError:
        raise NotFound(f"Post #{post_id} not found!")

    return render_template(
        "posts/post_detail.html",
        post_id=post_id,
        post_name=post_name,
    )
