import sqlite3

class Database():
    def DatabaseConnect(func):
        def Connect():
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            return func()
            conn.commit()
            cur.close()
        return Connect()


    def NewUser(id, lang):
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO users (user_id, language) VALUES (%s, '%s')" % (id, lang))
        conn.commit()
        cur.close()


    def SelectAll():
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        result = ''
        rows = cur.fetchall()
        for x in rows:
            result += str(x)
        result = result.replace(")", '\n')
        result = result.replace("(", "")
        cur.close()
        return result


    # NOT WORK
    def Recreate(self):
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute('DROP TABLE users')
        cur.execute('create table users (ID INTEGER PRIMARY KEY AUTOINCREMENT, USER_ID int, CITY text, LANGUAGE text)')


    def Language(id):
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("SELECT language FROM users WHERE user_id = %s" % id)
        lang = cur.fetchone()
        return lang[0]


    def City(id):
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("SELECT city FROM users WHERE user_id = %s" % id)
        city = cur.fetchone()
        return city[0]


    def DeleteUser(id):
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE user_id = %s" % id)
        conn.commit()
        cur.close()


    def UpdateLanguage(lang, id):
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("UPDATE users SET LANGUAGE = '%s' WHERE USER_ID = %s" % (lang, id))
        conn.commit()
        cur.close()


    def UpdateCity(city, id):
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("UPDATE users SET CITY = '%s' WHERE USER_ID = %s" % (city, id))
        conn.commit()
        cur.close()