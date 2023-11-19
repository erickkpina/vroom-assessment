from flask import Flask, render_template, flash, redirect, url_for, request
from database.database import db, migrate
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import uuid as uuid

from blueprints.posts.routes import posts_blueprint
from blueprints.users.routes import users_blueprint

from blueprints.users.models import Users
from blueprints.users.forms import LoginForm

from blueprints.users.forms import UserForm
from blueprints.users.models import Users
from api import api_blueprint


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/vroom'
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"


db.init_app(app)
migrate.init_app(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


app.register_blueprint(posts_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(api_blueprint)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # Check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Succesfull!!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password - Try Again!")
        else:
            flash("That User Doesn't Exist! Try Again...")

    return render_template('login.html', form=form, current_user=current_user)


@app.route('/user/add', methods=['GET', 'POST'])
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


@app.route('/dashboard', methods=['GET', 'POST'])
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


@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()

    try:
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
                               form=form, name=name, our_users=our_users)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!  Thanks For Stopping By...")
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True, port=3000)
