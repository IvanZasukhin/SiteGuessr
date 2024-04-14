import datetime

from flask import Flask, render_template, abort, redirect, make_response, jsonify, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

from data import db_session
from data import user_resource, website_resource, game_resources, statistic_resource
from data.users import User
from data.statistics import Statistic
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
    params = {"title": "Лучшие игроки",
              "users": [user for user in db_sess.query(User).all()]}
    return render_template("index.html", **params)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    params = {"title": "Авторизация",
              "form": form,
              }
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        params["message"] = "Неверный логин или пароль"
        return render_template('login.html', **params)
    return render_template('login.html', **params)


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
    params = {"title": "Регистрация",
              "form": form,
              }
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            params["message"] = "Пароли не совпадают"
            return render_template('register.html', **params)
        db_sess = db_session.create_session()
        user = User()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            params["message"] = "Уже есть такой пользователь"
            return render_template('register.html', **params)
        user.login = form.login.data
        user.description = form.description.data
        user.modified_date = datetime.datetime.now()
        user.created_date = datetime.datetime.now()
        user.set_password(form.password.data)
        db_sess.add(user)
        statistic = Statistic(user_id=user.id)
        user.statistic = statistic
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', **params)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/profile/<user_login>', methods=['GET', 'POST'])
def profile(user_login):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.login == user_login).first()
    params = {"title": "Профиль",
              "user": user}
    print(user.statistic.total_games)
    return render_template('profile.html', **params)


@app.route('/user/<user_login>', methods=['GET', 'POST'])
def edit_user(user_login):
    if not (current_user.is_authenticated or current_user.roles == "main admin"):
        return redirect("/")
    form = RegisterForm()
    params = {"title": "Изменения профиля",
              "form": form}
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == user_login).first()
        if user:
            form.login.data = user.login
            form.description.data = user.description
        else:
            abort(404)
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            params["message"] = "Пароли не совпадают"
            return render_template('register.html', **params)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == user_login).first()
        if user:
            if str(user.login) != str(form.login.data) and db_sess.query(User).filter(
                    User.login == form.login.data).first():
                params["message"] = "Уже есть такой пользователь"
                return render_template('register.html', **params)
            user.login = form.login.data
            user.description = form.description.data
            user.modified_date = datetime.datetime.now()
            user.set_password(form.password.data)
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('register.html', **params)


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

    app.run(port=8081, host='127.0.0.1')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    main()
