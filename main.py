from flask import Flask, redirect, render_template, session, request
from login_form import LoginForm
from users_model import UsersModel
from user_data_form import UserDataForm
from user_data_model import UserDataModel
from db import DB
from registration_form import RegistrationForm
from add_news_form import AddNewsForm
from news_model import NewsModel
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nothing'
db = DB()
UsersModel(db.get_connection()).init_table()
UserDataModel(db.get_connection()).init_table()
NewsModel(db.get_connection()).init_table()


@app.route('/')
def index():
    nm = NewsModel(db.get_connection())
    news = nm.get_all()
    if len(news) >= 3:
        new = [news[-1], news[-2], news[-3]]
    else:
        new = news
    if 'username' not in session:
        return render_template('index.html', text="Авторизироваться", news=new)
    return render_template('index.html', text='Личный кабинет', news=new, username=session['username'])


@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/<error>', methods=['GET', 'POST'])
def login(error=None):
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(user_name, password)
        if exists[0]:
            session['username'] = user_name
            session['user_id'] = exists[1]
        else:
            return redirect(
                '/login/notexist')
        return redirect("/")
    return render_template('login.html', title='Login', text="Авторизоваться", form=form,
                           error=error)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


@app.route('/registration', methods=["GET", "POST"])
@app.route('/registration/<er>', methods=["GET", "POST"])
def registration(er=None):
    form = RegistrationForm()
    if form.validate_on_submit():
        users = UsersModel(db.get_connection())
        udm = UserDataModel(db.get_connection())
        find = users.find(form.username.data)
        if find[0]:
            return redirect('/registration/exists')
        else:
            if form.username.data == 'admin':
                users.insert(form.username.data, form.password.data, 'admin')
            else:
                users.insert(form.username.data, form.password.data, 'user')  # add new user
            udm.insert(form.username.data, 'Фамилия', 'Имя', 'Отчество', 'Адрес', 'Номер счетчика')
            return redirect('/login')
    return render_template('registration.html', form=form, error=er, text="Авторизоваться")


@app.route('/system_info')
def info():
    if 'username' not in session:
        return render_template('info.html', text="Авторизироваться")
    return render_template('info.html', text='Личный кабинет')


@app.route('/profile')
def profile():
    udm = UserDataModel(db.get_connection())
    data = udm.get(session['username'])
    return render_template('profile.html', text="Личный кабинет", username=session['username'], data=data)


@app.route('/user_data', methods=["GET", "POST"])
def change_data():
    form = UserDataForm()
    udm = UserDataModel(db.get_connection())
    data = udm.get(session['username'])
    if form.validate_on_submit():
        udm.update(session['username'], form.surname.data, form.name.data, form.patronymic.data, form.address.data,
                   form.counter_number.data)
        data = udm.get(session['username'])
        if data[2] == 'Фамилия' or data[3] == 'Имя' or data[4] == 'Отчество' or data[5] == 'Адрес' or data[
            6] == 'Номер счетчика':
            return render_template('user_data.html', text="Личный кабинет", form=form, data=data, error='not_enough')
        return redirect('/profile')
    return render_template('user_data.html', text="Личный кабинет", form=form, data=data)


@app.route('/news_list', methods=["GET", "POST"])
def news_list():
    nm = NewsModel(db.get_connection())
    news = nm.get_all()
    return render_template('news_list.html', username=session['username'], news=news)


@app.route('/add_news', methods=["GET", "POST"])
def add_news():
    form = AddNewsForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        nm = NewsModel(db.get_connection())
        nm.insert(title, content)
        return redirect("/news_list")
    return render_template('add_news.html', username=session['username'], form=form)


@app.route('/del_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    nm = NewsModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/news_list")


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=False)
