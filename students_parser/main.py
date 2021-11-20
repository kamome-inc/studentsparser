import os
import sqlite3

dbname = 'first_test.db'


class Groups(object):
    """ """
    def __init__(self, group_name, subject, lesson_type, students):
        self.Name = group_name
        self.Subject = subject
        self.LessonType = lesson_type.strip()
        self.Students = students
        # Может быть использовать отдельный класс под студента с комментариями? хранить все в массиве?
        # не. Отдельная таблица и отдельный класс. Но тут пока что хранится массив студентов как обьектов класса

    def get_group(self):
        print("ГРУППА:-> ", self.Name, self.Subject, self.LessonType)
        for student in self.Students:
            student.get_student()

    def add_group_to_db(self):
        print(f"add group {self.Name}")
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        a = cur.execute("select * from Groups")
        a = a.fetchall()
        if len(a) > 0:
            lastindex = int(a[-1][0]) + 1  # возможны ошибки при удалении строк. ПРОВЕРЯЙ
        else:
            lastindex = 0
        cur.execute(f"Insert into Groups VALUES ({lastindex}, '{self.Name}', '{self.Subject}', '{self.LessonType}', '')")
        for student in self.Students:
            print(f"add student")
            cur.execute(student.add_student_to_db(lastindex))
        con.commit()
        con.close()


class Students(object):
    """ """
    def __init__(self,  name, comment):
        self.Name = name
        self.Comment = comment

    def get_student(self):
        print(self.Name)

    def add_student_to_db(self, group_id):
        return f"INSERT INTO StudentsInGroup (GroupId, Name, Comment) VALUES ({group_id}, '{self.Name}', '{self.Comment}')"


class Lessons(object):
    """class for all lessons"""
    def __init__(self, type, group, day, time, students):
        self.Type = type
        self.Group = group
        self.Date = day
        self.Time = time
        self.Students = students

    def get_lesson(self):
        print(self.Type, self.Group)
        print(self.Date, self.Time)
        print(self.Students)

    def set_students(self, strs):
        self.Students = strs

    def get_all_students(self):
        for i in self.Students:
            print(i)

    def clear_students(self):
        clear = []
        for student in self.Students[:]:
            if student.find(':') == -1:
                if student != '':
                    clear.append(' '.join(student.replace('+', '').replace('-', '').replace(',', '').split()))
        if not clear:
            self.Students = ["Студентов не было"]
        else:
            self.Students = list(set(clear))

    def add_lesson_to_db(self):
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        a = cur.execute("select * from Lessons")
        a = a.fetchall()
        if len(a) > 0:
            lastindex = int(a[-1][0])+1 # возможны ошибки при удалении строк. ПРОВЕРЯЙ
        else:
            lastindex = 0
        cur.execute(f"Insert into Lessons VALUES ({lastindex}, '{self.Type}', '{self.Group}', '{self.Date}', '{self.Time}')")
        con.commit()
        query = "Insert into STUDENTS  (LessonId, Student) VALUES "
        if len(self.Students) > 1:
            for student in self.Students[:-1]:
                query += f"({lastindex}, '{student}'), \n"
            query += f"({lastindex}, '{self.Students[-1]}') "
        else:
            query += f"({lastindex}, '{self.Students[0]}') "
        cur.execute(query)
        con.commit()
        con.close()


class GroopsFromDB(Groups):
    """Группы, только полученные из БД. Возможно вообще лишняя фигня. Потому что нахер надо. хз пока не юзать"""
    def __init__(self, id, group_name, subject, lesson_type, students):
        super().__init__(group_name, subject, lesson_type, students)
        self.Id = id

    def get_group_name(self):
        return self.Name

    def creation_from_sql(self):
        pass


def get_lessons_from_file(name_of_file, all_lessons):
    f = open(name_of_file, encoding="UTF8")
    input = f.readlines()
    pary = []

    lines = []
    for line in input:
        lines.append(line[:-1])
    # Проверка на корректность заполения файла. Если нет ни одного шаблона
    state = False
    statelist = list(map(lambda x: x == "Контактная информация для встречи в Google Meet", lines))
    for i in statelist:
        state = state or i

    if state:
        for i in range(len(lines)):
            # Выборка заголовка
            if lines[i] == "Контактная информация для встречи в Google Meet":
                if len(lines[i-2].split()) == 2:
                    type = lines[i-2].split()[0]
                    group = lines[i-2].split()[1]
                else:
                    type = ""
                    group = lines[i-2]
                day, time = lines[i-1].split(' · ') # Возможно что разделителя нормального в файле не будет
                index_begin = i+4
                #IndexEnd = list(map(lambda x: x == "Контактная информация для встречи в Google Meet", lines))
                pary.append([Lessons(type, group, day, time, ""), index_begin])

        if len(pary) == 1:
            pary[0].append(len(lines) - 1)
        else:
            for i in range(len(pary)-1):
                pary[i].append(pary[i+1][1]-6)
            pary[-1].append(len(lines)-1)

        for para in pary:
            para[0].set_students(list(set(lines[para[1]:para[2]])))
            all_lessons.append(para[0])
    else:
        print("ФАйл ", name_of_file, ' необходимо обработать вручную')


def get_groups_from_file(NameOfFile, ListOfGroups):
    f = open(NameOfFile, encoding="UTF8")
    f = f.readlines()
    ALLstudents = []
    for str in f[1:]:
        student = Students(str[:-1], "")
        ALLstudents.append(student)
    group, lesson, type = f[0][:-1].split("|")
    newgroup = Groups(group, lesson, type, ALLstudents)
    ListOfGroups.append(newgroup)


'''

# Это добавление списков групп в БД
ALLGroups = []
for root, dirs, files in os.walk('3'):
    for file in files:
        print(dirs, "FIle: ", file)
        get_groups_from_file('3\\' + file, ALLGroups)
for group in ALLGroups:
    group.add_group_to_db()


# А это считывание посещаемости и внесение ее в БД
AL = []
for root, dirs, files in os.walk('2'):
    for file in files:
        print(dirs, "FIle: ", file)
        get_lessons_from_file('2\\' + file, AL)
for lesson in AL:
    lesson.clear_students()
    lesson.get_lesson()
    lesson.add_lesson_to_db()
    

'''

