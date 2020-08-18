import psycopg2

conn = psycopg2.connect('dbname=jsinclair user=jsinclair')
cur = conn.cursor()

cur.execute('drop table if exists todos;')

cur.execute('''
    create table todos (
        id serial primary key,
        description varchar not null
    );
''')

descriptions = [
    'do some work',
    'do some more work',
    'drink a beer'
]
for description in descriptions:
    cur.execute(f"insert into todos (description) values('{description}');")

conn.commit()

cur.execute('SELECT * from todos;')

first_result = cur.fetchone()
cur.execute(
    f"insert into todos (description) values('{first_result[1].upper()}');")
conn.commit()

cur.execute('SELECT * from todos;')
all_results = cur.fetchall()

for row in all_results:
    print(row)

cur.close()
conn.close()
