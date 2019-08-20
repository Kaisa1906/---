class NewsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                title VARCHAR(128),
                                text VARCHAR(1000)
                                 )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, text):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO news 
                          (title, text) 
                          VALUES (?,?)''', (title, text))
        cursor.close()
        self.connection.commit()

    def get(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news WHERE id = ?", (str(news_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news")
        rows = cursor.fetchall()
        return rows

    def delete(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM news WHERE id = {}'''.format((str(news_id))))
        cursor.close()
        self.connection.commit()
