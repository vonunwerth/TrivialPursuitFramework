import codecs
import sqlite3
from sqlite3 import Error
from os import path


def create_connection(db_file):
    """
    Creates a connection to the database
    :param db_file: SQLite database file
    :return: Connection to the database
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)


def create_qac(conn, qac):
    """
    Inserts a QAC Triple to the Database
    :param conn: Connection to the database (file)
    :param qac: Question, Answer, Category Triple
    :return: Last inserted row id
    """
    sql = ''' INSERT INTO qac(question,answer,category)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, qac)
    return cur.lastrowid


def create_table(conn):
    """
    Creates the database table if not existing and adds a unique constraint for questions
    :param conn: Connection to the database
    :return: if finished
    """
    sql_create_table = '''create table qac (
    id integer primary key,
    question text not null,
    answer text not null,
    category text not null
);
'''
    sql_create_unique = '''create unique index qac_question_uindex on qac (question);'''  # make question unique
    cur = conn.cursor()
    cur.execute(sql_create_table)
    cur.execute(sql_create_unique)


def questions_to_database():
    """
    Write the questions from questions.txt to the database
    :return: if finished
    """
    db_existing = path.exists("python_sqlite.db")

    conn = create_connection("python_sqlite.db")
    if not db_existing:
        print("Created a new database for the questions! --> python_sqlite.db")
        create_table(conn)
    f = codecs.open("questions/questions.txt", "r", "utf-8")

    question = ""
    answer = ""
    category = ""

    qac_counter = 0
    question_counter = 0
    for line in f:
        if line.find("Q: ") >= 0:
            question = (line.split("Q: ")[1].split("\r\n")[0].split("\n")[0])  # All behind Q:, everything before \r\n or \n
            qac_counter = qac_counter + 1
        if line.find("A: ") >= 0:
            answer = (line.split("A: ")[1].split("\r\n")[0].split("\n")[0])
            qac_counter = qac_counter + 1
        if line.find("C: ") >= 0:
            category = (line.split("C: ")[1].split("\r\n")[0].split("\n")[0])
            qac_counter = qac_counter + 1
        if qac_counter == 3:  # on the same card
            with conn:  # Transaction
                try:
                    print("\033[92mQuestion: \033[1m" + question + "\033[0m \033[92m was saved as ID: "
                          + str(create_qac(conn, (question, answer, category)))
                          + "\033[92m in the database ./python_sqlite.db.")
                except sqlite3.IntegrityError:  # Integrity Error, when unique question is already in the db
                    print("\033[93mWarning: Question: \033[1m" + question + "\033[0m \033[93m was skipped. Already "
                                                                            "found in database. ")
            qac_counter = 0
            question_counter = question_counter + 1
    print("\033[0m")
    conn.close()


if __name__ == '__main__':
    questions_to_database()
