import psycopg2

def save_user_data(name, age):
    conn = psycopg2.connect(
        dbname="dars",
        user="postgres",
        password="1",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    cur.close()
    conn.close()
