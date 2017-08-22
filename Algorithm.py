from datetime import *
import sqlite3

# This is our connection to the database
conn = sqlite3.connect('activities.db')
# This is the cursor. Using it we can add, delete or update information in the database
c = conn.cursor()


def create_table():
    """
    This function creates a table with some columns that will be used later
    """
    c.execute('CREATE TABLE IF NOT EXISTS activities(name TEXT, sort TEXT, category TEXT, estimated_time_hours REAL, '
              'estimated_time_min REAL, '
              'ratio REAL, date_now TEXT, date TEXT, frm TEXT, till TEXT, priority REAL, status TEXT, score TEXT, '
              'frequency TEXT, Sunday TEXT, Monday TEXT, Tuesday TEXT, Wednesday TEXT, Thursday TEXT, Friday TEXT, '
              'Saturday TEXT)')
    data = strainer("", 'sort', 'category')
    if data == []:
        insert_category('None', 3)


def insert_todo(name, category, estimated_time_hours, estimated_time_min, day_when, priority, frequency):
    # date: Time when the user has made this activity. It'll work later as an id for the activity
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    # score: Score of the activity. If the score is smaller, the activity is more important
    # c.execute("SELECT priority FROM activities WHERE name=(?)"), [category]
    category_int = strainer('priority', 'name', category)
    score = int(len(frequency) + priority + category_int[0][0])

    # The next code will be adding the information to the database
    # First we tell the database in which table to put the info(here activities)
    # After that we tell him which variables we will be writing
    # Lastly we give him the variable

    c.execute("INSERT INTO activities (name, sort, category, estimated_time_hours, estimated_time_min, date_now, date, "
              "priority, score, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (name, 'todo', category, int(estimated_time_hours), int(estimated_time_min), now, day_when, priority,
               score, 'undone'))

    # Now we must commit the changes that happened in the database
    conn.commit()

    # The next bit of code will work at the frequency
    # This is a list of all days in the week written in capital just like the one's in the database
    list_of_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    # This for loop either puts in the column of the day a 1 if the activity will be done on that day. If not,
    # the loop will ignore it
    for i in list_of_days:
        if i in frequency:
            c.execute("UPDATE activities SET {} = 1 WHERE date_now=(?)".format(i), [now])
            c.execute("UPDATE activities SET frequency='correct' WHERE date_now=(?)", [now])
    # Now we must commit the changes that happened in the database
    conn.commit()


def insert_event(name, category, frm, to, day_when, priority, frequency):
    # date: Time when the user has made this activity. It'll work later as an id for the activity
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    # score: Score of the activity. If the score is smaller, the activity is more important
    # c.execute("SELECT priority FROM activities WHERE name=(?)"), [category]
    category_int = strainer('priority', 'name', category)
    score = len(frequency) + priority + category_int[0][0]

    # The next code will be adding the information to the database
    # First we tell the database in which table to put the info(here activities)
    # After that we tell him which variables we will be writing
    # Lastly we give him the variable

    c.execute("INSERT INTO activities (name, sort, category, frm, till, date_now, date, "
              "priority, score, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (name, 'event', category, frm, to, now, day_when, priority,
               score, 'undone'))

    # Now we must commit the changes that happened in the database
    conn.commit()

    # The next bit of code will work at the frequency
    # This is a list of all days in the week written in capital just like the one's in the database
    list_of_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    # This for loop either puts in the column of the day a 1 if the activity will be done on that day. If not,
    # the loop will ignore it
    for i in list_of_days:
        if i in frequency:
            c.execute("UPDATE activities SET {} = 1 WHERE date_now=(?)".format(i), [now])
            c.execute("UPDATE activities SET frequency='correct' WHERE date_now=(?)", [now])
    # Now we must commit the changes that happened in the database
    conn.commit()


def insert_category(name, priority):
    # The next code will be adding the information to the database
    # First we tell the database in which table to put the info(here activities)
    # After that we tell him which variables we will be writing
    # Lastly we give him the variable
    c.execute("INSERT INTO activities (name, sort, ratio, priority) VALUES (?, ?, ?, ?)",
              (name, 'category', 1, priority))
    # Now we must commit the changes that happened in the database
    conn.commit()


def edit(name, what, to):
    """
    Using this function, the user can edit anything he wants in the activity
    :param name: name of the activity
    :param what: what the user wants to change in the activity
    :param to: what that column should be
    """
    # Just like adding something, we use the cursor, but instead of INSERT INTO, we write UPDATE.
    # WHERE determines which activity the user wants to change
    c.execute("UPDATE activities SET {} = (?) WHERE name=(?)".format(what), [to, name])
    # Now we must commit the changes that happend in the database
    conn.commit()


def done(name):
    """
    This function marks an activity as done
    :param name: name of the activity
    """
    # This here works just like the updating function
    c.execute("UPDATE activities SET status = 'done' WHERE name=(?)", [name])
    conn.commit()


def delete(name):
    """
    This function deletes an activity from the database
    :param name: name of the activity
    """
    # Just like adding something, we use the cursor, but instead of INSERT INTO, we write DELETE FROM.
    # WHERE determines which activity the user wants to change
    c.execute("DELETE FROM activities WHERE name = (?)", [name])
    # Now we must commit the changes that happened in the database
    conn.commit()


def del_done():
    """
    This function deletes all of the done activities which don't repeat every now and then
    """
    # This function works just like the deleting function
    c.execute("DELETE FROM activities WHERE status = 'done' AND Frequency != 'correct'")
    conn.commit()


def strainer(select, strain, equals):
    """
    This function works as a strainer. Using it you can get something specific from the database
    :param select: Do you want to get all of the columns or only specific ones?
    :param strain: What should all things you want to see have in common?
    :param equals: What should it be equal to?
    :return a list of what the user wants to see
    """
    # This selects everything if the user didn't enter something for select
    if select == "":
        # Just like adding something, we use the cursor, but instead of INSERT INTO, we write DELETE FROM.
        # WHERE determines which activity the user wants to change
        c.execute("SELECT * FROM activities WHERE {}=(?)".format(strain), [equals])
        return c.fetchall()

    else:
        # Just like adding something, we use the cursor, but instead of INSERT INTO, we write DELETE FROM.
        # WHERE determines which activity the user wants to change
        c.execute("SELECT {} FROM activities WHERE {}=(?)".format(select.upper(), strain), [equals])
        return c.fetchall()


def organize(select, strain, equals):
    """
    This function returns a list of numbers. These numbers are the numbers of scores in a specific order. The first
    element is the most important one
    :parameters all of these parameters are used to get the scores of specific activities in the table!
    """
    scores = []
    data = list(strainer(select, strain, equals))
    while len(data) != 0:
        number = lowest_number(data)
        scores.append(number)
        data.remove(number)
    return scores


def lowest_number(list_int):
    """
    This function uses recursion to find the lowest number of a list
    :param list_int: list of int
    :return: smallest number
    """
    if len(list_int) == 1:
        return list_int[0]
    number = lowest_number(list_int[1:])
    if list_int[0] < number:
        return list_int[0]
    else:
        return number


def no_category():
    if len(strainer('', 'sort', 'category')) == 0:
        return False
    else:
        return True
