import os

db_path = 'website/database.db'

if os.path.exists(db_path):
    os.remove(db_path)
    print('Deleted existing database!')
else:
    print('No database file found.')