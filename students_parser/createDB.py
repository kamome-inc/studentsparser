import os
import sqlite3

dbname = 'first_test.db'

if os.path.isfile(dbname):
    os.remove(dbname)
    print("success")
else:
    print("File doesn't exists!")

con = sqlite3.connect(dbname)
cur = con.cursor()

cur.execute("""
            Create Table Lessons (
            Id INTEGER,
            Type text,
            LGroup text,
            Date text,
            Time text
            );
""")

cur.execute("""
            Create Table Students(
            Id INTEGER PRIMARY KEY autoincrement,
            LessonId,
            Student text);
""")

con.commit()

