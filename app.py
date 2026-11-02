
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table and insert sample data
def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT,
            branch TEXT,
            marks INTEGER
        )
    """)

    count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]

    if count == 0:
        conn.execute("""
            INSERT INTO students (name, branch, marks)
            VALUES
            ('Anu', 'CSE', 85),
            ('Ravi', 'ECE', 78),
            ('Priya', 'IT', 92)
        """)

    conn.commit()
    conn.close()

# Display student records
@app.route("/")
def home():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    return render_template("index.html", students=students)

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
