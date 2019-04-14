from flask import Flask, render_template, request, session, redirect, abort, send_file
from json import dumps

from backend.functions import *
from backend.forms import *
from database.db import *

app = Flask(__name__, template_folder='frontend', static_folder='frontend')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.errorhandler(403)
def who_are_you():
    return render_template('403.html')


@app.route('/')
@app.route('/index')
def index():
    if 'login' in session:
        return render_template('index.html')

    return redirect('/me')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if users_table.check_password(form.login.data, form.password.data) != 'error':
                session['login'] = form.login.data
                return redirect('/me')
            return dumps({'errors': 'Пользователь с таким логином и паролем не существует'})
        return render_template('login.html', title='Sign in', form=form)

    elif request.method == 'GET':
        return render_template('login.html', title='Sign in', form=form)

    else:
        answer = {'errors': 'Do not do this more',
                  'answer': None}

    return dumps(answer)


@app.route('/reg', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            if not users_table.get(form.login.data):
                users_table.insert(form.login.data, form.email.data, form.password1.data,
                                   form.name.data, form.surname.data, form.age.data, form.sex.data)

                session['login'] = form.login.data
                return redirect('/me')
            return dumps({'errors': 'Этот логин уже используется'})
        return render_template('reg.html', title='Registration', form=form)

    elif request.method == 'GET':
        return render_template('reg.html', title='Registration', form=form)

    else:
        abort(403)


@app.route('/me',  methods=['POST', 'GET'])
def me():
    if 'login' not in session:
        return redirect('/')

    if request.method == 'POST':
        pass

    elif request.method == 'GET':
        data = users_table.get(session['login'])

        return render_template('me.html', title=data['surname'] + " " + data['name'], data=data)


@app.route('/settings', methods=['POST', 'GET'])
def settings():
    if 'login' not in session:
        return redirect('/')

    form = SettingsForm()
    data = users_table.get(session['login'])
    if request.method == 'POST':
        if form.validate_on_submit():
            users_table.update(session['login'], form.email.data, form.password1.data, form.name.data,
                               form.surname.data, form.age.data, form.sex.data, form.image.data)

            return redirect('/me')
        return render_template('settings.html', title='Registration', form=form, data=data)

    elif request.method == 'GET':
        return render_template('settings.html', title='Настройки', form=form, data=data)


@app.route('/clubs', methods=['GET'])
def clubs():
    if 'login' not in session:
        return redirect('/')

    if request.method == 'GET':
        local = request.args.get('local')
        if local == 'me':
            data = clubs_table.get_for_user(session['login'])
            mode = ('all', 'Все кружки')

        elif local == 'all':
            data = clubs_table.get_all(('id', 'name', 'description', 'clubs_row'))
            mode = ('me', 'Мои кружки')

        else:
            return dumps({'error': 'exception arg'})

        return render_template('clubs.html', title='Кружки', data=data, mode=mode)


@app.route('/clubs/create', methods=['GET', 'POST'])
def create_club():
    if 'login' not in session:
        return redirect('/')

    form = CreateClubForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            dates = ','.join([str(form.monday.data), str(form.tuesday.data), str(form.wednesday.data),
                              str(form.thursday.data), str(form.friday.data), str(form.saturday.data),
                              str(form.monday.data)])

            clubs_table.insert(session['login'], form.name.data, form.description.data, form.address.data, dates,
                               form.image.data)

            return redirect('/clubs')
        return render_template('create_club.html', title='Кружки', form=form)

    elif request.method == 'GET':
        return render_template('create_club.html', title='Кружки', form=form)


@app.route('/image/<string:obj>/<string:id>', methods=['GET'])
def get_image(obj, id):
    if 'login' not in session:
        return dumps({'error': 'You are not user'})

    if obj == 'user':
        image = users_table.get_image(id)

    elif obj == 'club':
        image = clubs_table.get_image(id)

    else:
        image = 'standard.png'

    path = '/frontend/image/'

    return send_file(path + open_image_from_db(image))

#
# @app.route('/user/<int:user_id>', methods=['GET'])
# def profile(user_id):
#     if request.method == 'GET':
#         return render_template('profile.html', form=ProfileForm)
#
#


@app.route('/Logout')
def logout():
    if 'login' in session:
        session.pop('login')
    return redirect('/')


if __name__ == '__main__':
    database = DB()
    users_table = UsersTable(database.get_connection())
    clubs_table = ClubsTable(database.get_connection())
    clubs_table.init_table()
    app.run(port=8000, host='127.0.0.1')
