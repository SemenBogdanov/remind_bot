import psycopg2
from key import user, password, host, port


class BotDB:

    def __init__(self):
        """Инициализация подключения БД"""
        self.conn = psycopg2.connect(user=user,
                                     password=password,
                                     host=host,
                                     port=port,
                                     dbname='firstbase1')
        self.cur = self.conn.cursor()

    def get_all_records(self):
        """Получить все строки"""
        query = "select * from people;"
        self.cur.execute(query)
        res = self.cur.fetchall()
        return res

    def get_friends(self):
        """Получаем список друзей для проверки дней рождений"""
        query = "select persone_name, birthday_date from people;"
        self.cur.execute(query)
        res = self.cur.fetchall()
        print(res)
        return res

    def add_new_date(self, p_name, p_date):
        """Добавляем новую запись о дне рождения в таблицу"""
        try:
            query = """INSERT INTO people (persone_name, birthday_date) values (%s,%s)"""
            values = (str(p_name), str(p_date),)
            self.cur.execute(query, values)
            return True
        except:
            return False

    def getinfo(self):
        return self.conn.info

    def close(self, id):
        """Закрытие соединения с БД"""
        self.conn.close()
