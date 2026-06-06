from db import get_connection

conn = get_connection()
cur = conn.cursor()
cur.execute("SELECT condition_code FROM Condition;")
rows = cur.fetchall()
for row in rows:
    print(row)
cur.close()
conn.close()
print("Connection successful!")