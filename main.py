import datetime

from flask import Flask, render_template, abort, redirect, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

from data import db_session
from data import user_resource, website_resource, game_resources, statistic_resource
from data.users import User
from data.statistic import Statistic
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
    params = {"title": "Top players",
              "users": [user for user in db_sess.query(User).all()]}
    print(params["users"])
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
        session = db_session.create_session()
        user = User()
        if session.query(User).filter(User.login == form.login.data).first():
            return jsonify({'message': "There is already such a user"})
        user.login = form.login.data
        user.description = form.description.data
        user.modified_date = datetime.datetime.now()
        user.created_date = datetime.datetime.now()
        user.set_password(form.password.data)
        session.add(user)
        statistic = Statistic()
        user.statistic = statistic
        session.commit()
        return redirect('/login')
    return render_template('register.html', **params)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not current_user.is_authenticated:
        return redirect("/")
    params = {"title": "Registration",
              "statistic": current_user.statistic}
    return render_template('profile.html', **params)


def main():
    db_session.global_init("db/site_guessr.db")

    api.add_resource(user_resource.UserListResource, '/api/users')
    api.add_resource(user_resource.UserResource, '/api/user/<int:users_id>')

    api.add_resource(website_resource.WebsiteListResource, '/api/websites')
    api.add_resource(website_resource.WebsiteResource, '/api/website/<int:website_id>')

    api.add_resource(game_resources.GameListResource, '/api/games')
    api.add_resource(game_resources.GameResource, '/api/game/<int:game_id>')

    api.add_resource(statistic_resource.StatisticListResource, '/api/statistic')
    api.add_resource(statistic_resource.StatisticResource, '/api/statistic/<int:game_id>')

    app.run(port=8080, host='127.0.0.1')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    main()
