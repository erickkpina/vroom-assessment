from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc
from werkzeug.utils import secure_filename
import uuid as uuid
import os

from .forms import PostForm, SearchForm
from .models import Posts

from database.database import db

posts_blueprint = Blueprint('posts', __name__, template_folder='/templates')


@posts_blueprint.route('/')
def posts():
    page = request.args.get("page", 1, type=int)
    posts = Posts.query.order_by(desc(Posts.date_posted)).paginate(
        page=page, per_page=5
    )

    if request.headers.get("Accept") == "application/json":
        postsJson = [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "post_image": post.post_image,
                "date_posted": post.date_posted.strftime("%Y/%m/%d - %H:%M"),
            }
            for post in posts.items
        ]
        return jsonify(postsJson)
    else:
        return render_template("posts.html", posts=posts, current_user=current_user)


@posts_blueprint.route('/posts/<int:id>')
def getPost(id):
    post = Posts.query.get_or_404(id)
    if request.headers.get("Accept") == "application/json":
        postsJson = [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "post_image": post.post_image,
                "date_posted": post.date_posted.strftime("%Y/%m/%d - %H:%M"),
            }
            for post in posts.items
        ]
        return jsonify(postsJson)
    else:
        return render_template('post.html', post=post, current_user=current_user)


@posts_blueprint.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()

    if request.method == "POST":
        author_id = current_user.id
        postImage = None

        if form.validate_on_submit():
            if form.image.data:
                imageName = secure_filename(str(uuid.uuid4()) + ".jpg")
                form.image.data.save(f"static/images/{imageName}")
                imagePath = f"/{imageName}"

                postImage = imagePath
            else:
                flash("Sem imagem")

        post = Posts(
            title=form.title.data,
            content=form.content.data,
            author_id=author_id,
            post_image=postImage
        )

        flash("Blog Post Submitted Successfully!")
    else:
        return render_template("add_post.html", form=form)

    try:
        db.session.add(post)
        db.session.commit()
        return redirect("/")
    except:
        flash("Error! Looks like there was a problem...try again!")
        return render_template("add_post.html", form=form)


@posts_blueprint.route('/posts/edit/<int:id>', methods=['GET', 'POST', 'PUT'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm(obj=post)

    if request.method == "POST":
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data

            if form.image.data:
                imageName = secure_filename(str(uuid.uuid4()) + ".jpg")
                form.image.data.save(f"static/images/{imageName}")
                imagePath = f"/{imageName}"

                post.post_image = imagePath

            # db.session.add(post)
            db.session.commit()
            flash("Post Has Been Updated!")

    elif request.method == "PUT":
        data = request.get_json()

        if not data:
            return jsonify({'message': 'No data provided'}), 400

        if 'title' in data:
            post.title = data['title']
        if 'content' in data:
            post.content = data['content']

        if 'image' in data:
            imageName = secure_filename(str(uuid.uuid4()) + ".jpg")
            data['image'].save(f"static/images/{imageName}")
            imagePath = f"/{imageName}"
            post.post_image = imagePath

        try:
            db.session.commit()
            return jsonify({'message': 'Post updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error updating post', 'error': str(e)}), 500
    else:
        return render_template("edit_post.html", form=form, post=post)

    try:
        db.session.commit()
        return redirect("/")
    except:
        flash("Error! Looks like there was a problem...try again!")
        return render_template("edit_post.html", form=form, post=post)


@posts_blueprint.route('/posts/delete/<int:id>', methods=['DELETE'])
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()

        # Return a message
        flash("Post Was Deleted!")
        return redirect("/")

    except:
        # Return an error message
        flash("There was a problem deleting this post")
        return redirect("/")


@posts_blueprint.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@posts_blueprint.route('/search', methods=["POST"])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        # Get data from submitted form
        getPost.searched = form.searched.data
        # Query the Database
        posts = posts.filter(Posts.title.like('%' + getPost.searched + '%'))
        posts = posts.order_by(Posts.title).all()

        return render_template("search.html",
                               form=form,
                               searched=getPost.searched,
                               posts=posts)
