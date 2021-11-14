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


# В новой версии эта вспомогательная таблица будет удалена.
cur.execute("""
            Create Table Students(
            Id INTEGER PRIMARY KEY autoincrement,
            LessonId,
            Student text);
""")


cur.execute("""
            Create Table Groups(
            ID int,
            GroupName text,
            Subject text,
            LessonType text,
            GroupSameName text)
""")

cur.execute("""
            Create Table StudentsInGroup (
            ID INTEGER PRIMARY KEY autoincrement,
            GroupId int,
            Name text,
            Comment text
            )
""")


cur.execute("""
            CREATE Table Attendance (
            ID INTEGER PRIMARY KEY autoincrement,
            GroupId int,
            StudentInGroupId int,
            Comment text)
            
""")
con.commit()

