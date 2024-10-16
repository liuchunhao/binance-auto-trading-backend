import sqlite3
import os
import datetime
import logging

logging.basicConfig(level=logging.INFO)

# insert mt5 balance to database
def insert_mt5_balance(db_file='database/crypto.sqlite3', margin=0.0, balance=0.0):
    print(os.getcwd())
    conn = None
    try:
        os.makedirs(os.path.dirname(db_file), exist_ok=True)

        # create db file if not exist but do not truncate if exist
        with open(db_file, 'a') as f:  # append mode
            pass
        
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()                         

        # create table called mt5_balance that has column date, time, margin, balance if not exist
        cur.execute('CREATE TABLE IF NOT EXISTS mt5_balance (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, time TEXT, margin REAL, balance REAL)')
        conn.commit()

        # insert data into table
        cur.execute('INSERT INTO mt5_balance (date, time, margin, balance) VALUES (?, ?, ?, ?)', (datetime.datetime.now().strftime('%Y-%m-%d'), datetime.datetime.now().strftime('%H:%M:%S'), margin, balance))
        conn.commit()

        # select data from table
        cur.execute('SELECT * FROM mt5_balance order by id desc limit 1')
        rows = cur.fetchall()
        for row in rows:
            print(row)

        conn.close()
    except Exception as e:
        print(e)

# select latest mt5 balance from database
def select_latest_mt5_balance(db_file='database/crypto.sqlite3'):
    udate = ''
    utime = ''
    margin = 0.0
    balance = 0.0
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()                         
        # select data from table
        cur.execute('SELECT * FROM mt5_balance order by id desc limit 1')
        rows = cur.fetchall()
        for row in rows:
            udate = row[1]
            utime = row[2]
            margin = row[3]
            balance = row[4]
            print(row)
        conn.close()
    except Exception as e:
        logging.error(e)
    return udate, utime, margin, balance

if __name__ == '__main__':
    # insert_mt5_balance()
    udate, utime, margin, balance = select_latest_mt5_balance()
    print(f'margin: {margin}, balance: {balance}')