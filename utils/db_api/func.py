from sqlite3 import Error
import sqlite3
from time import ctime
from datetime import datetime
from xlsxwriter.workbook import Workbook

class DBS:
    def post_sql_query(sql_query):
        with sqlite3.connect('./my.db') as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(sql_query)
            except Error:
                pass
            result = cursor.fetchall()
            return result


    def create_tables(self):
        users_query = '''CREATE TABLE IF NOT EXISTS USERS
                            (user_id INTEGER PRIMARY KEY NOT NULL,
                            username TEXT,
                            first_name TEXT,
                            last_name TEXT,
                            lang TEXT,
                            full_name TEXT,
                            reg_date TEXT);'''

        self.post_sql_query(users_query)
        
    def register_user(self, user, username, first_name, last_name):
        user_check_query = f'SELECT * FROM USERS WHERE user_id = {user};'
        user_check_data = self.post_sql_query(user_check_query)
        if not user_check_data:
            insert_to_db_query = f'INSERT INTO USERS (user_id, username, first_name,  last_name, reg_date) VALUES ' \
                                f'({user}, "{username}", "{first_name}", "{last_name}", "{ctime()}");'
            self.post_sql_query(insert_to_db_query)

    def set_user_lang(self, user_id, lang):
        lang_query = f"UPDATE USERS set lang='{lang}' where user_id={user_id}"
        self.post_sql_query(lang_query)

    def user_lang(self, user_id):
        user_check_query = f'SELECT lang FROM USERS WHERE user_id = {user_id};'
        user_check_data = self.post_sql_query(user_check_query)[0][0]
        if user_check_data == None:
            return False
        return user_check_data
    
    def user_fullname(self, user_id):
        user_check_query = f'SELECT full_name FROM USERS WHERE user_id = {user_id};'
        user_check_data = self.post_sql_query(user_check_query)[0][0]
        if user_check_data == None:
            return False
        return user_check_data
    
    def set_user_fullname(self, user_id, fullname):
        lang_query = f"UPDATE USERS set full_name='{fullname}' where user_id={user_id}"
        self.post_sql_query(lang_query)

    
    def user_list(self):
        query = "SELECT * FROM USERS"
        data = self.post_sql_query(query)
        return data

    def _set_olimpiada(self, name, answer, start, end):
        arr = str(start).split(' ')
        arr2 = str(end).split(' ')
        query = 'INSERT INTO olimpiada(name, answer, start, end, start_time, end_time) VALUES' \
            f'("{name}", "{answer}", (date("{arr[0]}")), (date("{arr2[0]}")), (time("{arr[1]}")), (time("{arr2[1]}")))'
        self.post_sql_query(query)
    
    def _start_user_olimpiada(self):
        date = datetime.now().strftime("%Y-%m-%d")
        _time = datetime.now().strftime("%H:%M")
        query = f"SELECT * FROM olimpiada WHERE start >= '{date}' and 'end' >= '{date}' and end_time >= time('{_time}') and start_time <= time('{_time}')"
        data = self.post_sql_query(query)
        return data
        
    def get_olimpiada(self):
        date = datetime.now().strftime("%Y-%m-%d")
        _time = datetime.now().strftime("%H:%M")
        query = f"SELECT * FROM olimpiada WHERE start >= '{date}' and 'end' >= '{date}' and end_time >= '{_time}'"
        data = self.post_sql_query(query)
        return data
    
    def ByOlimpiada(self, _id):
        date = datetime.now().strftime("%Y-%m-%d")
        _time = datetime.now().strftime("%H:%M")
        query = f"SELECT * FROM olimpiada WHERE start >= '{date}' and 'end' >= '{date}' and end_time >= time('{_time}') and start_time <= time('{_time}') and id={_id}"
        data = self.post_sql_query(query)
        return data

    def delete_olimpiada(self, olimpiada_id):
        query = f"DELETE FROM olimpiada WHERE id={olimpiada_id}"
        self.post_sql_query(query)

    def _check_rank(self, user_id, olimpiada_id)-> bool:
        query = f"SELECT * FROM olimpiada_rank WHERE user_id='{user_id}' and olimpiada_id='{olimpiada_id}'"
        data = self.post_sql_query(query)
        if len(data) == 0: return True 
        else: return False

    def _set_rank(self, user_id, olimpiada_id, check):
        _time = datetime.now().strftime("%H:%M:%S")
        fullname = self.post_sql_query(f"SELECT full_name FROM USERS where user_id={user_id}")[0][0]
        print(fullname)
        query = 'INSERT INTO olimpiada_rank("user_id","full_name", "olimpiada_id", "check", "send_time") VALUES' \
            f'("{user_id}", "{fullname}", "{olimpiada_id}", "{check}", time("{_time}"))'
        print(query)
        self.post_sql_query(query)

    def _get_rank(self):
        query = 'SELECT  * FROM olimpiada_rank ORDER BY  "check" DESC, "send_time" ASC'
        data = self.post_sql_query(query)
    
    def _set_new_channel(self, channel_id, link):
        query = f'INSERT INTO channels(channel_id, link) VALUES ("{channel_id}", "{link}")'
        self.post_sql_query(query)
    
    def _get_channels(self):
        return self.post_sql_query("SELECT channel_id, link FROM channels")
    
    def _delete_channel(self, channel_id):
        return self.post_sql_query(f"DELETE FROM channels WHERE channel_id='{channel_id}';")

    def get_xls(self, olimpiada_id):
        workbook = Workbook('rank.xlsx')
        worksheet = workbook.add_worksheet()

        conn=sqlite3.connect('my.db')
        c=conn.cursor()
        c.execute(f'SELECT  * FROM olimpiada_rank WHERE olimpiada_id="{olimpiada_id}" ORDER BY  "check" DESC, "send_time" ASC')
        data = c.fetchall()
        print(data)
        if data== None: return False
        f1=workbook.add_format({'bold':True, 'border':1, 'border_color': 'black', 'align':'center'})
        f2=workbook.add_format({'border':1, 'border_color':'black', 'align':'center'})
        worksheet.write_row('A1', ['reyting','user_id', 'full_name', 'olimpida_id', 'procent', 'send_time'], f1)
        for i, row in enumerate(data):
            print(row[1])
            i+=1
            worksheet.write(i, 0, i, f2)
            worksheet.write(i, 1, row[1], f2)
            worksheet.write(i, 2, row[2], f2)
            worksheet.write(i, 3, row[3], f2)
            worksheet.write(i, 4, row[4], f2)
            worksheet.write(i, 5, row[5], f2)
        worksheet.set_column('A:A', 11)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 40)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 20)
        worksheet.set_column('F:F', 20)
        workbook.close()

# migrate
db = DBS()
