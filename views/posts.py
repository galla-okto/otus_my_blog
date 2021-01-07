from flask import Blueprint, render_template, request, redirect, url_for

from models import Post
from models.database import db

post_app = Blueprint("post_app", __name__)

@post_app.route("/", endpoint='posts_list')
def posts_list():
    posts = Post.query.filter_by(deleted=False).all()
    return render_template("posts/post_list.html", posts=posts)

@post_app.route("/<int:post_id>", endpoint='post_detail')
def post_detail(post_id):
    post = Post.get_post_by_id(post_id)

    return render_template(
        "posts/post_detail.html",
        post=post,
    )

@post_app.route("/<int:post_id>/delete", methods=["POST"], endpoint='post_delete')
def post_delete(post_id):
    post = Post.get_post_by_id(post_id)
    post.deleted = True
    db.session.commit()
    return redirect(url_for("post_app.posts_list"))

@post_app.route("/add/", methods=["POST", "GET"], endpoint='add_post')
def post_add():
    if request.method == "GET":
        return render_template("posts/add_post.html")

    post_name = request.form.get("post_name")
    is_new = bool(request.form.get("is-new"))
    post = Post(name=post_name, is_new=is_new)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for("post_app.posts_list"))
