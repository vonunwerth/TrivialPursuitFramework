# coding=utf-8
import codecs
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)


def create_qac(connection, qac):
    sql = ''' INSERT INTO qac(question,answer,category)
              VALUES(?,?,?) '''
    cur = connection.cursor()
    cur.execute(sql, qac)
    return cur.lastrowid


conn = create_connection("pythonsqlite.db")
f = codecs.open("questions.txt", "r", "utf-8")

question = ""
answer = ""
category = ""

qac_counter = 0
question_counter = 0
for x in f:
    if x.find("Q: ") >= 0:
        question = (x.split("Q: ")[1].split("\r\n")[0])  # All behind Q:, everything before \r\n
        qac_counter = qac_counter + 1
    if x.find("A: ") >= 0:
        answer = (x.split("A: ")[1].split("\r\n")[0])
        qac_counter = qac_counter + 1
    if x.find("C: ") >= 0:
        category = (x.split("C: ")[1].split("\r\n")[0])
        qac_counter = qac_counter + 1
    if qac_counter == 3: # TODO suhffle all questions, that those that are behind each other in the txt are not on the same card
        with conn: # Transaction
            try:
                print "Frage: \033[1m" + question + " wurde als ID: " + str(create_qac(conn, (question, answer, category))) + "in die Datenbank eingetragen" # TODO englisch
            except sqlite3.IntegrityError: # Integrity Error, wenn Unique Frage bereits enthalten ist.
                print "Frage: \033[1m" + question + "\033[0m wurde uebersprungen. Sie ist bereits in der Datenbank enthalten."
        qac_counter = 0
        question_counter = question_counter + 1

conn.close()