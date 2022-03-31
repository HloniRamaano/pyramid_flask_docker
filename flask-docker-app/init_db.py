import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="to_do_list",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'],
        port=5430)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS lists;')
cur.execute('CREATE TABLE lists (id serial PRIMARY KEY,'
                                 'item varchar (150) NOT NULL);'
                                 )

# Insert data into the table

cur.execute('INSERT INTO lists (item)'
            'VALUES (%s);',
            ('A Tale of Two Cities',))

cur.execute('INSERT INTO lists (item)'
            'VALUES (%s);',
            ('Bob the builder',))

cur.execute('INSERT INTO lists (item)'
            'VALUES (%s);',
            ('Disney',))


# cur.execute('INSERT INTO books (title, author, pages_num, review)'
#             'VALUES (%s, %s, %s, %s)',
#             ('Anna Karenina',
#              'Leo Tolstoy',
#              864,
#              'Another great classic!')
#             )

conn.commit()

cur.close()
conn.close()