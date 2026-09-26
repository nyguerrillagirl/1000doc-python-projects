import psycopg2

conn = psycopg2.connect(
    dbname="datacampdb",
    user="datacamp",
    password="PASSWORD_HERE",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

cur.execute("""
    DELETE FROM students
    WHERE inter_dom IS NULL;
""")

conn.commit()

cur.close()
conn.close()
