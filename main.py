import datetime

from flask import Flask, render_template, abort, redirect, make_response, jsonify, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from sqlalchemy import desc

from data import db_session
from data import user_resource, website_resource, game_resources, statistic_resource
from data.statistics import Statistic
from data.users import User
from data.websites import Website
from forms.user_change_password import ChangePasswordForm
from forms.user_edit_profile import EditProfileForm
from forms.user_login import LoginForm
from forms.user_register import RegisterForm
from forms.website_register import WebsiteRegisterForm

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandex_lyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    params = {"title": "Лучшие игроки",
              "users": [user for user in
                        db_sess.query(User).join(Statistic).filter(User.banned == 0).order_by(
                            desc(Statistic.correct_answers), desc(User.login)).limit(10).all()]}
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
        statistic = Statistic()
        statistic.user_id = user.id
        user.statistic = statistic
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', **params)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/banned/<int:user_id>', methods=['GET'])
def banned_user(user_id):
    if current_user.role != 'main admin' and current_user.banned != 1:
        redirect("/")
    if current_user.id == user_id:
        return redirect(f"/profile/{current_user.login}")
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    user.banned = True
    db_sess.commit()
    return redirect(f"/profile/{user.login}")


@app.route('/unbanned/<int:user_id>', methods=['GET'])
def unbanned_user(user_id):
    if current_user.role != 'main admin' and current_user.banned != 1:
        redirect("/")
    if current_user.login == user_id:
        return redirect(f"/profile/{current_user.login}")
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    user.banned = False
    db_sess.commit()
    return redirect(f"/profile/{user.login}")


@app.route('/profile/<user_login>', methods=['GET', 'POST'])
@login_required
def profile(user_login):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.login == user_login).first()
    params = {"title": "Профиль",
              "user": user}
    return render_template('profile.html', **params)


@app.route('/user/<user_login>', methods=['GET', 'POST'])
@login_required
def edit_user(user_login):
    if not (current_user.login == user_login or (current_user.role == "main admin" and current_user.banned != 1)):
        return redirect("/")
    form = EditProfileForm()
    params = {"title": "Изменения профиля",
              "form": form}
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == user_login).first()
        params["user"] = user
        if user:
            form.login.data = user.login
            form.description.data = user.description
            form.role.data = user.role
            form.total_games.data = user.statistic.total_games
            form.correct_answers.data = user.statistic.correct_answers
            form.wrong_answers.data = user.statistic.wrong_answers
            form.average_score.data = user.statistic.average_score
            form.best_score.data = user.statistic.best_score
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == user_login).first()
        params["user"] = user
        if user:
            if (str(user.login) != str(form.login.data) and
                    db_sess.query(User).filter(User.login == form.login.data).first()):
                params["message"] = "Такое имя пользователя занято"
                return render_template('edit_profile.html', **params)
            if form.login.data:
                user.login = form.login.data
            user.description = form.description.data
            user.modified_date = datetime.datetime.now()
            if form.role.data:
                user.role = form.role.data
            user.statistic.total_games = form.total_games.data
            user.statistic.correct_answers = form.correct_answers.data
            user.statistic.wrong_answers = form.wrong_answers.data
            user.statistic.average_score = form.average_score.data
            user.statistic.best_score = form.best_score.data
            db_sess.commit()
            return redirect(f'/profile/{user_login}')
        else:
            abort(404)
    else:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == user_login).first()
        params["user"] = user
    return render_template('edit_profile.html', **params)


@app.route('/websites', methods=['GET', 'POST'])
@login_required
def websites():
    if not (current_user.role == 'admin' or (current_user.role == 'main admin' and current_user.banned != 1)):
        return redirect("/")
    db_sess = db_session.create_session()
    params = {"title": "База сайтов",
              "websites": [user for user in
                           db_sess.query(Website).join(User).all()]}
    return render_template("websites.html", **params)


@app.route('/change_password/<user_login>', methods=['GET', 'POST'])
@login_required
def change_password(user_login):
    if not current_user.login == user_login:
        return redirect("/")
    form = ChangePasswordForm()
    params = {"title": "Регистрация",
              "form": form,
              }
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            params["message"] = "Пароли не совпадают"
            return render_template('change_password.html', **params)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == user_login).first()
        if not user.check_password(form.old_password.data):
            params["message"] = "Был введён неверный пароль"
            return render_template('register.html', **params)
        user.set_password(form.password.data)
        db_sess.commit()
        return redirect(f'/profile/{user_login}')
    return render_template('change_password.html', **params)


@app.route('/user', methods=['GET', 'POST'])
@login_required
def all_users():
    if not (current_user.role == "main admin" and current_user.banned != 1):
        return redirect("/")
    db_sess = db_session.create_session()
    params = {"title": "Все пользователи",
              "users": [user for user in
                        db_sess.query(User).order_by(
                            desc(User.login), desc(User.login)).all()]}
    return render_template("all_users.html", **params)


@app.route('/website', methods=['GET', 'POST'])
@login_required
def website_register():
    if not ((current_user.role == "admin" or current_user.role == "main admin") and current_user.banned != 1):
        return redirect("/")
    form = WebsiteRegisterForm()
    params = {"title": "Добавление веб-сайта",
              "form": form,
              }
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        website = Website()
        if db_sess.query(Website).filter((Website.name == form.name.data) | (Website.url == form.url.data)).first():
            params["message"] = "Уже есть такой сайт"
            return render_template('website.html', **params)
        website.name = form.name.data
        website.url = form.url.data
        website.user_id = current_user.id
        db_sess.add(website)
        db_sess.commit()
        return redirect('/websites')
    return render_template("website.html", **params)


@app.route('/website/<int:website_id>', methods=['GET', 'POST'])
@login_required
def website_edit(website_id):
    if not ((current_user.role == "admin" or current_user.role == "main admin") and current_user.banned != 1):
        return redirect("/")
    form = WebsiteRegisterForm()
    params = {"title": "Изменения веб-сайта",
              "form": form}
    if request.method == "GET":
        db_sess = db_session.create_session()
        website = db_sess.query(Website).get(website_id)
        if website:
            form.name.data = website.name
            form.url.data = website.url
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        website = db_sess.query(Website).get(website_id)
        if website:
            website.name = form.name.data
            website.url = form.url.data
            db_sess.commit()
            return redirect(f'/websites')
        else:
            abort(404)
    return render_template('website.html', **params)


@app.route('/website_delete/<int:website_id>', methods=['GET', 'POST'])
@login_required
def website_delete(website_id):
    db_sess = db_session.create_session()
    if current_user.role == 'main admin' and current_user.banned != 1:
        website = db_sess.query(Website).get(website_id)
    else:
        website = db_sess.query(Website).filter(Website.id == website_id,
                                                Website.user == current_user).first()
    if website:
        db_sess.delete(website)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/websites')


def main():
    db_session.global_init("db/site_guessr.db")

    api.add_resource(user_resource.UserListResource, '/api/users')
    api.add_resource(user_resource.UserResource, '/api/user/<int:users_id>')

    api.add_resource(website_resource.WebsiteListResource, '/api/websites.html')
    api.add_resource(website_resource.WebsiteResource, '/api/website/<int:website_id>')

    api.add_resource(game_resources.GameListResource, '/api/games')
    api.add_resource(game_resources.GameResource, '/api/game/<int:game_id>')

    api.add_resource(statistic_resource.StatisticListResource, '/api/statistic')
    api.add_resource(statistic_resource.StatisticResource, '/api/statistic/<int:game_id>')

    app.run(port=8088, host='127.0.0.1')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    main()
