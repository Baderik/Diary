from database.db import *

if __name__ == '__main__':
    database = DB()

    users_table = UsersTable(database.get_connection())
    users_table.init_table()

    clubs_table = ClubsTable(database.get_connection())
    clubs_table.init_table()
