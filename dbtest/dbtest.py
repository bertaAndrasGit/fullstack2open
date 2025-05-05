import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS testdatabase")

cursor.close()
conn.close()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="testdatabase"
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    expert BOOLEAN NOT NULL,
    admin BOOLEAN NOT NULL
);
""")

cursor.execute("""
INSERT INTO users (name, password, expert, admin)
VALUES ('András', 'mypassword', true, false)
""")
conn.commit()  


cursor.execute("SELECT * FROM users")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()