# Create database
# Run command: `python3 scripts/db-create.py`

import mysql.connector
import config as c

db = mysql.connector.connect(host=c.DB_HOST, user=c.DB_USER, password=c.DB_PASSWORD)
cursor = db.cursor()
cursor.execute("SHOW DATABASES")

dbExists = False
for x in cursor:
    if c.DB_NAME in x:
        dbExists = True
if dbExists:
    print(f'Database "{c.DB_NAME}" already exists!')
else: 
    cursor.execute(f"CREATE DATABASE {c.DB_NAME}")
    