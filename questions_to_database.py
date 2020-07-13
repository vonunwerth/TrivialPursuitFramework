# coding=utf-8
import codecs
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)


def create_qac(conn, qac):
    sql = ''' INSERT INTO qac(question,answer,category)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, qac)
    return cur.lastrowid


def questions_to_database():
    conn = create_connection("python_sqlite.db")
    f = codecs.open("questions/questions.txt", "r", "utf-8")

    question = ""
    answer = ""
    category = ""

    qac_counter = 0
    question_counter = 0
    for line in f:
        if line.find("Q: ") >= 0:
            question = (line.split("Q: ")[1].split("\r\n")[0])  # All behind Q:, everything before \r\n
            qac_counter = qac_counter + 1
        if line.find("A: ") >= 0:
            answer = (line.split("A: ")[1].split("\r\n")[0])
            qac_counter = qac_counter + 1
        if line.find("C: ") >= 0:
            category = (line.split("C: ")[1].split("\r\n")[0])
            qac_counter = qac_counter + 1
        if qac_counter == 3:
            # on the same card # TODO Verify all questions have a category and are with short enough size etc!
            with conn:  # Transaction
                try:
                    print "\033[92mQuestion: \033[1m" + question + "\033[0m \033[92m was saved as ID: " \
                          + str(create_qac(conn, (question, answer, category))) \
                          + "\033[92m in the database ./python_sqlite.db."
                except sqlite3.IntegrityError:  # Integrity Error, wenn Unique Frage bereits enthalten ist.
                    print "\033[93mWarning: Question: \033[1m" + question + "\033[0m \033[93mwas skipped. Already " \
                                                                            "found in database. "
            qac_counter = 0
            question_counter = question_counter + 1
    print "\033[0m"
    conn.close()


if __name__ == '__main__':
    questions_to_database()
