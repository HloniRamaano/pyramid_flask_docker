import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="to_do_list",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'],
        port=5430)

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS lists;')
cur.execute('CREATE TABLE lists (id serial PRIMARY KEY,'
                                 'item varchar (150) NOT NULL);'
                                 )

# Populate the table

cur.execute('INSERT INTO lists (item)'
            'VALUES (%s);',
            ('Apple',))

cur.execute('INSERT INTO lists (item)'
            'VALUES (%s);',
            ('Banana',))

conn.commit()

cur.close()
conn.close()