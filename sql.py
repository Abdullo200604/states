import psycopg2

conn = psycopg2.connect("dbname=dars user=postgres password=1")
cur = conn.cursor()

# cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar(30));")

# Ma'lumot qo'shish (TO'G'RI)
cur.execute("INSERT INTO test(num, data) VALUES (20, 'va alaykum assalom');")

conn.commit()

cur.close()
conn.close()


def add_user():
    return None