import json

import flask
from data import db_session, users
from data.__all_models import RegisterForm, LoginForm, ItemsForm
from data.allitems import Items1
from data.item import Items
from data.jobs import Jobs
from data.users import User
from flask import Flask, render_template, session, redirect
from flask import request, make_response, jsonify
from flask_login import LoginManager, login_required, logout_user
from flask_login import login_manager, login_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init('db/blogs.db')
login_manager = LoginManager()
login_manager.init_app(app)
blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/register", methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('index2.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('index2.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('index2.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/additem', methods=['GET', 'POST'])
def add():
    form = ItemsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        item = db_sess.query(Items1).filter(Items1.name == form.name.data).first()
        if item and current_user.admin:
            item.howm += form.howm.data
            db_sess.commit()
            return redirect("/")
        elif not item and current_user.admin:
            db_sess.add(Items1(
                name=form.name.data,
                price=form.price.data,
                about=form.about.data,
                howm=form.howm.data
            ))
            db_sess.commit()
            return redirect("/")
        return render_template('index.html',
                               message="Неправильные данные",
                               form=form)
    return render_template('index.html', title='Авторизация', form=form)


@app.route('/bag')
def bag():
    a2 = db_session.create_session()
    a3 = a2.query(Items).filter(Items.leader == current_user.id).all()
    return render_template("work.html", j=a3)


@app.route('/addtobag/<int:numb>')
def addbag(numb):
    a2 = db_session.create_session()
    a1 = a2.query(Items1).filter(Items1.id == numb).first()
    a = Items(
        name=a1.name,
        price=a1.price,
        about=a1.about,
        howm=a1.howm,
        leader=current_user.id
    )
    a2.add(a)
    a2.commit()
    return redirect("/")


@app.route('/deletebag/<int:num>')
def delbag(num):
    a2 = db_session.create_session()
    a3 = a2.query(Items).filter(Items.id == num and Items.leader == current_user.id).first()
    a2.delete(a3)
    a2.commit()
    return redirect("/bag")


@app.route('/delete/<int:numm>')
def delit(numm):
    a2 = db_session.create_session()
    a3 = a2.query(Items1).filter(Items1.id == numm).first()
    a2.delete(a3)
    a2.commit()
    return redirect("/")


@app.route('/')
def maina():
    db_sess = db_session.create_session()
    j1 = db_sess.query(Items1).all()
    return render_template("main.html", j=j1)


@blueprint.route('/api/items')
def get_items():
    db_sess = db_session.create_session()
    items = db_sess.query(Items).all()
    return jsonify(
        {
            'items':
                [item.to_dict(only=('name', 'price', 'about', 'howm'))
                 for item in items]
        }
    )


@blueprint.route('/api/items/<int:item_id>', methods=['GET'])
def get_one_item(item_id):
    db_sess = db_session.create_session()
    item = db_sess.query(News).get(item_id)
    if not news:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'items':
                [item.to_dict(only=('name', 'price', 'about', 'howm'))
                 ]
        }
    )


@blueprint.route('/api/items', methods=['POST'])
def create_items():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'price', 'about', 'howm']):
        return jsonify({'error': 'Bad request'})
    elif not current_user:
        return jsonify({'error': 'Not login'})
    db_sess = db_session.create_session()
    items = Items1(
        name=request.json['name'],
        price=request.json['price'],
        about=request.json['about'],
        howm=request.json['howm'],
    )
    db_sess.add(items)
    db_sess.commit()
    return jsonify({'success': 'OK'})


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

# магаз сайт с api
