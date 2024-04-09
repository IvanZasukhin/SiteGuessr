import datetime

from flask import Flask, render_template, redirect, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from requests import post
from sqlalchemy.exc import IntegrityError

from data import db_session
from data import user_resource, website_resource, game_resources
from data.users import User
from forms.job import Job
from forms.user_login import LoginForm
from forms.user_register import RegisterForm

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandex_lyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    # jobs = db_sess.query(Job)
    params = {"title": "Work log",
              }
    return render_template("index.html", **params)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Incorrect login or password",
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect("/")
    form = RegisterForm()
    params = {"title": "Registration",
              "form": form,
              }
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            params["message"] = "Password mismatch"
            return render_template('register.html', **params)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            params["message"] = "There is already such a user"
            return render_template('register.html', **params)
        post(f'http://localhost:8080/api/users', json={'login': form.login.data,
                                                       'description': form.description.data,
                                                       'hashed_password': form.hashed_password.data}).json()
        return redirect('/')
    return render_template('register.html', **params)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/blogs.db")
    # try:
    #     db_sess = db_session.create_session()
    #     creating_user(db_sess)
    # except IntegrityError:
    #     pass

    api.add_resource(user_resource.UsersListResource, '/api/users')
    api.add_resource(user_resource.UsersResource, '/api/user/<int:users_id>')

    api.add_resource(website_resource.WebsiteListResource, '/api/websites')
    api.add_resource(website_resource.WebsiteResource, '/api/website/<int:website_id>')

    api.add_resource(game_resources.GameListResource, '/api/games')
    api.add_resource(game_resources.GameResource, '/api/game/<int:game_id>')

    app.run(port=8080, host='127.0.0.1')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def creating_user(db_sess):
    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    user.set_password("1234")
    db_sess.add(user)

    user = User()
    user.surname = "Zas"
    user.name = "Ivan"
    user.age = 17
    user.position = "assistant captain"
    user.speciality = "engineer"
    user.address = "module_2"
    user.email = "ivan1@mars.org"
    user.set_password("1234")
    db_sess.add(user)

    user = User()
    user.surname = "Zas2"
    user.name = "Ivan2"
    user.age = 18
    user.position = "assistant captain"
    user.speciality = "engineer"
    user.address = "module_3"
    user.email = "ivan2@mars.org"
    user.set_password("1234")
    db_sess.add(user)

    user = User()
    user.surname = "Zas3"
    user.name = "Ivan3"
    user.age = 19
    user.position = "assistant captain"
    user.speciality = "engineer"
    user.address = "module_3"
    user.email = "ivan3@mars.org"
    user.set_password("1234")
    db_sess.add(user)

    job = Job()
    job.user = db_sess.query(User).filter(User.id == 1).first()
    job.job = "deployment of residential modules 1 and 2"
    job.work_size = 15
    job.collaborators = "2, 3"
    job.start_date = datetime.datetime.now()
    job.is_finished = False
    db_sess.add(job)

    job = Job()
    job.user = db_sess.query(User).filter(User.id == 3).first()
    job.job = "deployment of residential modules 1"
    job.work_size = 9
    job.collaborators = "2"
    job.start_date = datetime.datetime.now()
    job.is_finished = True
    db_sess.add(job)

    db_sess.commit()


if __name__ == '__main__':
    main()
