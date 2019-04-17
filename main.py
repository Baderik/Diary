from flask import Flask, render_template, request, session, redirect, send_file
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
        return redirect('/me')

    return render_template('index.html')


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


@app.route('/me',  methods=['GET'])
def me():
    if 'login' not in session:
        return redirect('/')

    if request.method == 'GET':
        week = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье')
        data = users_table.get(session['login'])
        week_grp = {_: list() for _ in range(7)}
        # print(clubs_table.get_for_user(session['login'], ('id', 'name', 'dates')))

        for grp in clubs_table.get_for_user(session['login'], ('id', 'name', 'dates')):
            # print(grp)
            days = grp['dates'].split(',')

            for day in range(7):
                week_grp[day] = week_grp.get(day, []) + ([grp['name']] if eval(days[day]) else [])
        # print(week_grp)

        return render_template('me.html', title=data['surname'] + " " + data['name'], data=data,
                               week_grp=week_grp, week=week)


@app.route('/settings', methods=['POST', 'GET'])
def settings():
    if 'login' not in session:
        return redirect('/')

    form = SettingsForm()
    data = users_table.get(session['login'])
    if request.method == 'POST':
        if form.validate_on_submit():

            image = form.image.data.read() if form.image.data else ''

            users_table.update(session['login'], form.email.data, form.password1.data, form.name.data,
                               form.surname.data, form.age.data, form.sex.data, image)

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
                              str(form.sunday.data)])
            # print(dates)
            image = form.image.data.read() if form.image.data else ''

            clubs_table.insert(session['login'], form.name.data, form.description.data, form.address.data, dates, image)

            return redirect('/clubs?local=me')
        return render_template('create_club.html', title='Кружки', form=form)

    elif request.method == 'GET':
        return render_template('create_club.html', title='Кружки', form=form)


@app.route('/clubs/<int:club_id>', methods=['GET', 'POST'])
def club(club_id):
    if 'login' not in session:
        return redirect('/')

    data = clubs_table.get(club_id, ('id', 'login', 'name', 'description', 'membership', 'clubs_row', 'dates'))
    data['admin'] = users_table.get(data['login'], ('name',))['name'] + ' ' + \
                    users_table.get(data['login'], ('surname',))['surname']
    week = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье')
    # print(data['dates'])
    data['dates'] = ', '.join([week[day] for day in range(7) if data['dates'].split(',')[day] == 'True'])

    del week

    member = '❌' if session['login'] + ',' in data['membership'] else '✔'
    login = session['login']

    form = ClubForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if member == '✔':
                # member = '❌'
                clubs_table.add_user(club_id, session['login'])

            else:
                # member = '✔'
                clubs_table.del_user(club_id, session['login'])
                # print(clubs_table.get(club_id, ('membership',)))
                # print(session['login'])

            return redirect(f'/clubs/{club_id}')
        return render_template('club.html', title=data['name'], form=form, member=member, data=data, user=login)

    elif request.method == 'GET':
        return render_template('club.html', title=data['name'], form=form, member=member, data=data, user=login)


@app.route('/clubs/<int:club_id>/settings', methods=['GET', 'POST'])
def club_settings(club_id):
    data = clubs_table.get(club_id)
    week = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    dates = data['dates'].split(',')

    for day in range(7):
        data[week[day]] = eval(dates[day])

    del week
    del data['dates']
    # print(data)

    if 'login' not in session or session['login'] != data['login']:
        return redirect('/')

    form = ClubSettingsForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            dates = ','.join([str(form.monday.data), str(form.tuesday.data), str(form.wednesday.data),
                              str(form.thursday.data), str(form.friday.data), str(form.saturday.data),
                              str(form.sunday.data)])
            # print(dates)
            image = form.image.data.read() if form.image.data else ''

            clubs_table.update(club_id, form.name.data, form.description.data, dates, image)

            return redirect(f'/clubs/{club_id}')
        return render_template('club_settings.html', title='Настройки', form=form, data=data)

    elif request.method == 'GET':
        return render_template('club_settings.html', title='Настройки', form=form, data=data)


@app.route('/image/<string:obj>/<string:id>', methods=['GET'])
def get_image_from_db(obj, id):
    if 'login' not in session:
        return dumps({'error': 'You are not user'})

    if obj == 'user':
        image = users_table.get_image(id)

    elif obj == 'club':
        image = clubs_table.get_image(id)

    else:
        image = 'standard.png'

    path = 'frontend/image/'

    return send_file(path + open_image_from_db(image))


@app.route('/image/<string:name>', methods=['GET'])
def get_image(name):
    if 'login' not in session:
        return dumps({'error': 'You are not user'})

    path = 'frontend/image/'

    return send_file(path + name)


@app.route('/Logout')
def logout():
    if 'login' in session:
        session.pop('login')
    return redirect('/')


@app.route('/Del/<string:mode>/<string:id>')
def del_user(mode, id):
    if 'login' in session:
        if mode == 'user':
            users_table.delete(id)
            if session['login'] == id:
                session.pop('login')

            return redirect('/')

        elif mode == 'group':
            clubs_table.delete(id)
            return redirect('/clubs?local=me')

    return redirect('/')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


if __name__ == '__main__':
    database = DB()
    users_table = UsersTable(database.get_connection())
    clubs_table = ClubsTable(database.get_connection())
    clubs_table.init_table()
    app.run(port=8000, host='127.0.0.1')
