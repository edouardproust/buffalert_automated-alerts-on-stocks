# Create database
# Run command: `python3 scripts/db-create.py`

import mysql.connector
import config as c

db = mysql.connector.connect(host=c.DB_HOST, user=c.DB_USER, password=c.DB_USER_PASSWORD)
cursor = db.cursor()
cursor.execute("SHOW DATABASES")

dbExists = False
for x in cursor:
    if c.DB in x:
        dbExists = True
if dbExists:
    print(f'Database "{c.DB}" already exists!')
else: 
    cursor.execute(f"CREATE DATABASE {c.DB}")
    