from main import Lessons, Students, Groups
import os
import sqlite3

dbname = 'first_test.db'
con = sqlite3.connect(dbname)
cur = con.cursor()


a = cur.execute("select * from Lessons")
# for i in range len a...
for a in a.fetchall():
    #a = a.fetchone()
    i, type, group, day, time = a
    if type == "":
        type = "Лабораторная работа"
    else:
        type = "Лекция"

    lecstrings = []

    ex = cur.execute(f"select Student from Students WHERE LessonId = {i}")
    ex = ex.fetchall()
    for str in ex:
        #print(str[0])
        lecstrings.append(str[0].lower())

    lesson = Lessons(type, group, day, time, lecstrings)

    #lesson.get_lesson()


    a = cur.execute("select Id, GroupName from Groups WHERE LessonType = 'Лекции'")
    a = a.fetchall()

    SetGroup = set(lesson.Group)
    #print(SetGroup)
    MaxMatch = 0
    MaxId = None
    i = 0
    for id, groupname in a:
        SetGroupName = set(groupname)

        if len(SetGroup & SetGroupName) > MaxMatch:
            MaxMatch = len(SetGroup & SetGroupName)
            MaxId = i
        elif len(SetGroup & SetGroupName) == MaxMatch:
            print("EXCEPTION!!!")
        i += 1
        #print(id, groupname, SetGroupName, len(SetGroup & SetGroupName))
    #print(a[MaxId], MaxId)
    if MaxId == None:
        print("NotFound!!!")
        continue
    else:
        GroupId = a[MaxId][0]
        print(a[MaxId][1], ' = ', lesson.Group)


'''
st = cur.execute(f"Select Name FROM StudentsInGroup WHERE GroupId = {GroupId}")
st = st.fetchall()
print(st)
'''
'''


def search_by_group_name(Lesson:Lessons, GroupNames):
    pass


def search_student():
    pass



a = cur.execute("select GroupName, LessonType from Groups WHERE LessonType = 'Лекции'")
a = a.fetchall()
for i in a:
   pass# print(i)
'''