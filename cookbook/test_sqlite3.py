import sqlite3
import os

stocks = [
    ('GOOG', 100, 490.1),
    ('APPL', 50, 545.75),
    ('FB', 150, 7.45),
    ('HPQ', 75, 33.2),
]

db_file = 'tmp/database.db'
abs_path = os.path.abspath('.')
abs_db_path = os.path.join(abs_path, db_file)
print('{}, {}'.format(abs_path, abs_db_path))

if not os.path.exists(abs_db_path):
    db = sqlite3.connect(abs_db_path)
    print('create db')
    c = db.cursor()
    c.execute('CREATE TABLE portfolio (symbol TEXT, shares INTEGER, price REAL)')
    c.executemany('INSERT INTO portfolio VALUES (?,?,?)', stocks)
    db.commit()
else:
    print('db data:')
    db = sqlite3.connect(abs_db_path)
    is_null = True
    rows = db.execute('SELECT * FROM portfolio')
    if rows.arraysize > 0:
        for row in rows:
            print(row)
