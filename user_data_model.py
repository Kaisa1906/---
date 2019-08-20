class UserDataModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users_data 
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    username VARCHAR(50),
                                     surname VARCHAR(50),
                                     name VARCHAR(50),
                                     patronymic VARCHAR(50),
                                     address VARCHAR(256),
                                     counter_number VARCHAR(128)
                                     )''')
        cursor.close()
        self.connection.commit()

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users_data")
        rows = cursor.fetchall()
        return rows

    def insert(self, username, surname, name, patronymic, address, counter_number):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users_data 
                          (username,surname, name, patronymic, address, counter_number) 
                          VALUES (?,?,?,?,?,?)''', (username, surname, name, patronymic, address, counter_number))
        cursor.close()
        self.connection.commit()

    def delete(self, username):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM users_data WHERE username = ?''', (username,))
        cursor.close()
        self.connection.commit()

    def get(self, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users_data WHERE username = ?", (username,))
        row = cursor.fetchone()
        return row

    def update(self, username, surname=None, name=None, patronymic=None, address=None, counter_number=None):
        cursor = self.connection.cursor()
        if surname:
            cursor.execute('''UPDATE users_data SET surname = ? WHERE username = ?''', (surname, username,))
        if name:
            cursor.execute('''UPDATE users_data SET name = ? WHERE username = ?''', (name, username,))
        if patronymic:
            cursor.execute('''UPDATE users_data SET patronymic = ? WHERE username = ?''', (patronymic, username,))
        if address:
            cursor.execute('''UPDATE users_data SET address = ? WHERE username = ?''', (address, username,))
        if counter_number:
            cursor.execute('''UPDATE users_data SET counter_number = ? WHERE username = ?''', (counter_number, username,))
        cursor.close()
        self.connection.commit()
