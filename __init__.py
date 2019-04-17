from database.db import *

if __name__ == '__main__':
    database = DB()

    users_table = UsersTable(database.get_connection())
    users_table.init_table()

    users_table.insert("Petr_gamer", "petr@game.com", "petr_gamer", "Пётр", "Лосев", 16, "мужской")
    users_table.insert("Utka", "baderik@yandex.ru", "utka", "Павел", "Бадерик", 16, "мужской")
    users_table.insert("Fox", "fox@vk.com", "fox", "Михаил", "Бадерик", 16, "мужской")
    users_table.insert("Nikolay", "nikol@gmail.com", "nikolay", "Николай", "Моргунов", 16, "мужской")
    users_table.insert("Vasiliy", "vasy@mail.ru", "vasiliy", "Василий", "Шибаев", 16, "мужской")

    clubs_table = ClubsTable(database.get_connection())
    clubs_table.init_table()

    clubs_table.insert("Petr_gamer", "Red Dead Redemption", "GG", "'ARENA'", "False,False,False,False,False,True,True",
                       '')
    clubs_table.insert("Nikolay", "Яндекс.Лицей", "Python", "ГЭК", "True,False,False,False,True,False,False", '')
    clubs_table.insert("Vasiliy", "Google", "...", "Where?", "True,True,True,True,True,False,False", '')
    clubs_table.insert("Utka", "Yandex", "Я", "Russia", "True,True,True,True,True,False,False", '')
    clubs_table.insert("Fox", "DuckDuckGo", "Open source", "Anywhere", "True,True,True,True,True,True,True", '')



