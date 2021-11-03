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

    def getinfo(self):
        return self.conn.info

    def close(self, id):
        """Закрытие соединения с БД"""
        self.conn.close()
