from passlib.hash import pbkdf2_sha256
from sqlite3 import connect, OperationalError


class DB:
    def __init__(self):
        try:
            self.conn = connect('../database/diary.db', check_same_thread=False)

        except OperationalError:
            self.conn = connect('database/diary.db', check_same_thread=False)

    def get_connection(self):
        return self.conn

    def __del__(self):
        try:
            self.conn.close()

        except AttributeError:
            print("haven't conn")


class UsersTable:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             login VARCHAR(25) UNIQUE,
                             email VARCHAR(25),
                             password_hash VARCHAR(100),
                             name TEXT,
                             surname TEXT,
                             age INTEGER,
                             sex VARCHAR(25),
                             image BLOB
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, login, email, password, name, surname, age, sex):
        # print('User:\n', login, email, password, name, surname, age, sex)
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (login, email, password_hash, name, surname, age, sex) 
                          VALUES (?,?,?,?,?,?,?)''', (login, email, pbkdf2_sha256.hash(password),
                                                      name, surname, age, sex))
        cursor.close()
        self.connection.commit()

    def update(self, login, email, password, name, surname, age, sex, image):
        headers = ['email', 'name', 'surname', 'age', 'sex']
        data = [email, name, surname, age, sex]

        if password:
            headers.append('password_hash')
            data.append(password)

        if image:
            headers.append('image')
            data.append(image)

        cursor = self.connection.cursor()
        cursor.execute(f'''UPDATE users
                           SET {" = ?, ".join(headers) + '= ?'}
                           WHERE login = ?''', data + [str(login)])

        cursor.close()
        self.connection.commit()

    def get(self, login, headers=None):
        if headers is None:
            headers = ('login', 'email', 'name', 'surname', 'age', 'sex')

        cursor = self.connection.cursor()

        cursor.execute(f'''SELECT {", ".join(headers)}
                          FROM users WHERE login = ?''', (str(login),))
        row = cursor.fetchone()
        if row:
            row = {headers[i]: row[i] for i in range(len(headers))}
        return row

    def get_password(self, login):
        cursor = self.connection   .cursor()
        cursor.execute('''SELECT password_hash
                          FROM users WHERE login = ?''', (str(login),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT user_name FROM users")
        rows = cursor.fetchall()
        return rows

    def get_image(self, login):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT image
                                  FROM users WHERE login = ?''', (str(login),))
        row = cursor.fetchone()
        return row

    def check_password(self, login, password):
        row = self.get_password(login)
        answer = 'error'

        if row and pbkdf2_sha256.verify(password, row[0]):
            answer = 'success'

        return answer

    def delete(self, login):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM users WHERE login = ?''', (login,))
        cursor.close()
        self.connection.commit()


class ClubsTable:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS clubs 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             login VARCHAR(25),
                             name VARCHAR(50),
                             description TEXT,
                             membership TEXT,
                             clubs_row INTEGER,
                             address VARCHAR(30),
                             dates TEXT,
                             image BLOB
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, login, name, description, address, dates, image):
        # print('Club:\n', login, name, description, address, dates, image)
        cursor = self.connection.cursor()

        cursor.execute('''INSERT INTO clubs 
                            (login, name, description, membership, clubs_row, address, dates, image) 
                            VALUES (?,?,?,?,?,?,?,?)''', (login, name, description,
                                                          login+',', 1, address, dates, image))

        cursor.close()
        self.connection.commit()

    def update(self, club_id, name, description, dates, image):
        headers = ['name', 'description', 'dates']
        data = [name, description, dates]

        if image:
            headers.append('image')
            data.append(image)

        cursor = self.connection.cursor()
        cursor.execute(f'''UPDATE clubs
                           SET {" = ?, ".join(headers) + '= ?'}
                           WHERE id = ?''', data + [str(club_id)])

        cursor.close()
        self.connection.commit()

    def get(self, club_id, headers=None):
        cursor = self.connection.cursor()

        if headers is None:
            headers = ('id', 'login', 'name', 'description', 'address', 'dates', 'clubs_row')

        cursor.execute(f'''SELECT {", ".join(headers)}
                                  FROM clubs WHERE id = ?''', (str(club_id),))
        row = cursor.fetchone()
        if row:
            row = {headers[i]: row[i] for i in range(len(headers))}
        # print(row)
        return row

    def get_all(self, headers=None):
        cursor = self.connection.cursor()

        if headers is None:
            headers = ('name', 'description', 'dates', 'clubs_row')

        cursor.execute(f'''SELECT {", ".join(headers)} FROM clubs''')
        row = cursor.fetchall()
        if row:
            row = [{headers[i]: obj[i] for i in range(len(headers))} for obj in row]
        return row

    def get_for_user(self, user_login, headers=None):
        user_login += ','
        if headers is None:
            headers = ('id', 'name', 'description', 'clubs_row')
        data = self.get_all(('id', 'membership'))

        if data:
            # print(data)
            data = [self.get(grp['id'], headers)
                    for grp in data if user_login in grp['membership']]
            # print(data)
        return data

    def add_user(self, club_id, user_login):
        data = self.get(club_id, ('membership', 'clubs_row'))
        membership, clubs_row = data['membership'], data['clubs_row']
        user_login += ','

        if not membership:
            membership = ''

        cursor = self.connection.cursor()
        if user_login not in membership:
            membership += user_login
            clubs_row += 1

            cursor.execute('''UPDATE clubs
                              SET membership = ?, clubs_row = ?
                              WHERE id = ?''', (membership, clubs_row, str(club_id)))

        cursor.close()
        self.connection.commit()

    def del_user(self, club_id, user_login):
        data = self.get(club_id, ('membership', 'clubs_row'))
        membership, clubs_row = data['membership'], data['clubs_row']
        user_login += ','

        if not membership:
            membership = ''

        cursor = self.connection.cursor()
        if user_login in membership:
            membership = membership.replace(user_login, '')
            clubs_row -= 1

            cursor.execute('''UPDATE clubs
                              SET membership = ?, clubs_row = ?
                              WHERE id = ?''', (membership, clubs_row, str(club_id)))

        cursor.close()
        self.connection.commit()

    def get_image(self, clubs_id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT image
                                  FROM clubs WHERE id = ?''', (str(clubs_id),))
        row = cursor.fetchone()
        return row

    def delete(self, club_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM clubs WHERE id = ?''', (str(club_id),))
        cursor.close()
        self.connection.commit()
