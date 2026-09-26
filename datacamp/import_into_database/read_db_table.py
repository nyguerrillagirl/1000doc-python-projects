import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="datacampdb",
    user="datacamp",
    password="PASSWORD_HERE",
    host="localhost",
    port="5432"
)

# Create a cursor
cur = conn.cursor()

# Execute a query
cur.execute("SELECT * FROM students;")

# Fetch all rows
rows = cur.fetchall()

# Print results
for row in rows:
    print(row)

column_names = [desc[0] for desc in cur.description]

print(column_names)

# Clean up
cur.close()
conn.close()
