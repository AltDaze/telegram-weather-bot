import sqlite3

class Database():
    def DatabaseConnect(func):
        def Connect(*args):
            with sqlite3.connect('users.db') as conn:
                cursor = conn.cursor()
                function = func(*args, cursor)
                conn.commit()
                return function
        return Connect


    @DatabaseConnect
    def NewUser(user_id, lang, cur):
        cur.execute("INSERT INTO users (user_id, language) VALUES (%s, '%s')" % (user_id, lang))


    @DatabaseConnect
    def SelectAll(cur):
        cur.execute("SELECT * FROM users")
        result = [row for row in cur.fetchall()]
        replaces = {
            "),": "\n",
            ")": "",
            "(": "",
            "[": "",
            "]": ""}
        for i, j in replaces.items(): result = result.replace(i, j)
        return result



    @DatabaseConnect
    def Language(user_id, cur):
        cur.execute("SELECT language FROM users WHERE user_id = %s" % user_id)
        lang = cur.fetchone()
        return lang[0]


    @DatabaseConnect
    def City(user_id, cur):
        cur.execute("SELECT city FROM users WHERE user_id = %s" % user_id)
        city = cur.fetchone()
        return city[0]


    @DatabaseConnect
    def DeleteUser(user_id, cur):
        cur.execute("DELETE FROM users WHERE user_id = %s" % user_id)


    @DatabaseConnect
    def UpdateLanguage(lang, user_id, cur):
        cur.execute("UPDATE users SET LANGUAGE = '%s' WHERE USER_ID = %s" % (lang, user_id))


    @DatabaseConnect
    def UpdateCity(city, user_id, cur):
        cur.execute("UPDATE users SET CITY = '%s' WHERE USER_ID = %s" % (city, user_id))
    

    # NOT WORK
    def Recreate(self):
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute('DROP TABLE users')
        cur.execute('create table users (ID INTEGER PRIMARY KEY AUTOINCREMENT, USER_ID int, CITY text, LANGUAGE text)')
