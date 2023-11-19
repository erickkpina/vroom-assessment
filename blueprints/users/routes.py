from flask import Blueprint, render_template, flash, request
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import uuid as uuid

from database.database import db

from .forms import UserForm
from .models import Users
from ..posts.models import Posts

users_blueprint = Blueprint('users', __name__, template_folder='/templates')


@users_blueprint.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(
                form.password_hash.data)
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data,
                         favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''

        flash("User Added Successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",
                           form=form,
                           name=name,
                           our_users=our_users)


@users_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    userToUpdate = Users.query.get_or_404(id)

    if request.method == "POST":
        userToUpdate.name = request.form['name']
        userToUpdate.email = request.form['email']
        userToUpdate.favorite_color = request.form['favorite_color']
        userToUpdate.username = request.form['username']
        userToUpdate.about_author = request.form['about_author']

        if form.profile_pic.data:
            imageName = secure_filename(str(uuid.uuid4()) + ".jpg")
            form.profile_pic.data.save(f"static/images/{imageName}")
            imagePath = f"/{imageName}"

            userToUpdate.profile_pic = imagePath

            try:
                db.session.commit()
                flash("User Updated Successfully!")
                return render_template("dashboard.html",
                                       form=form,
                                       userToUpdate=userToUpdate)
            except:
                flash("Error!  Looks like there was a problem...try again!")
                return render_template("dashboard.html",
                                       form=form,
                                       userToUpdate=userToUpdate)
        else:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("dashboard.html",
                                   form=form,
                                   userToUpdate=userToUpdate)
    else:
        return render_template("dashboard.html",
                               form=form,
                               userToUpdate=userToUpdate,
                               id=id)


@users_blueprint.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()

    try:
        db.session.query(Posts).filter_by(author_id=user_to_delete.id).delete()
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!!")

        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html",
                               form=form,
                               name=name,
                               our_users=our_users)

    except:
        flash("Whoops! There was a problem deleting user, try again...")
        return render_template("add_user.html",
                               form=form, name=name)
