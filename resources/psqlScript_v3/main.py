# coding=utf-8
from psycopg2 import connect
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

db_found = False

con = connect(user='postgres', host='localhost', password='postgres')

dbname = sys.argv[1]

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()

cur.execute('SELECT * FROM pg_catalog.pg_database')
results = cur.fetchall() # bring all dbs in server

for item in results:
    if dbname in item[0]:
        db_found = True
        break

if db_found is False:
    cur.execute('CREATE DATABASE ' + '"' + dbname + '"')
else:
    print('You already have a database called ' + dbname + ', trying to connect to it')
cur.close()
con.close()

con = connect(user='postgres', dbname=dbname, host='localhost', password='postgres')
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()

cur.execute('DROP TABLE IF EXISTS Appointments CASCADE')

cur.execute('CREATE TABLE Appointments(id SERIAL PRIMARY KEY NOT NULL, name VARCHAR(255) NOT NULL, date BIGINT NOT NULL, created_date BIGINT NOT NULL, sent BOOLEAN, voice_alerted BOOLEAN)')

print('Script finished successfully')
cur.close()
con.close()