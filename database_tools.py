import sqlite3

import database_statistics
from constants import ANSWER_MAX_LINE_LENGTH, QUESTION_MAX_LINE_LENGTH


def create_connection(db_file):
    """
    Create a database connection to a SQLite database
    :param db_file: SQLite database file
    :return: Connection to the database
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except sqlite3.Error as e:
        print(e)


def validate_questions():
    """
    Validates question entries on its length, if they have a questions mark at the end, ...
    :return: Warning and Error count
    """
    print "Validating question entries..."
    conn = create_connection("python_sqlite.db")
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id,question FROM qac ORDER BY id")
        error_count = 0
        warning_count = 0
        for entry in cur.fetchall():
            question_id = entry[0]
            question = entry[1]
            any_error_or_warning = False
            if len(
                    question) > 3 * QUESTION_MAX_LINE_LENGTH:
                print "\033[91mError: Question of entry with ID: " + str(
                    question_id) + " is to long! Cards will be ugly! \033[0m" + question + " \033[91mHas length: " + \
                      str(len(question)) + "/" + str(3 * QUESTION_MAX_LINE_LENGTH) + "\033[0m"
                error_count = error_count + 1
                any_error_or_warning = True
            if question[-1] != "?" and question[-3:] != "...":  # Question mark or citing ...s are missing
                any_error_or_warning = True
                warning_count = warning_count + 1  #
                if question[-1] == " ":
                    print "\033[93mWarning: Question of entry with ID: " + str(
                        question_id) + " has spaces attached to the back. \033[0m" + question
                else:
                    print "\033[93mWarning: Question of entry with ID: " + str(
                        question_id) + " has not a ? or ... as last symbol! \033[0m" + question
            if any_error_or_warning:
                print("")  # Organize Errors and Warnings in blocks grouped by id

        print "\033[1mQuestion-Report\n\033[0m\033[91m  Errors found: \033[0m\033[1m" + str(
            error_count) + "\n \033[0m\033[93m Warnings found: \033[0m\033[1m" + str(warning_count) + "\033[0m\n"
        return warning_count, error_count


def validate_answers():
    """
    Validates the answer entries, if they are to long, ...
    :return: Warning and Error count
    """
    print "Validating answer entries..."
    conn = create_connection("python_sqlite.db")
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id,answer,category FROM qac ORDER BY id")
        error_count = 0
        warning_count = 0
        for entry in cur.fetchall():
            answer_id = entry[0]
            answer = entry[1]
            any_error_or_warning = False
            if len(answer.split("(")[0]) > 2 * ANSWER_MAX_LINE_LENGTH:  # if both lines of the answer are to long in sum
                print "\033[91mError: Answer of entry with ID: " + str(
                    answer_id) + " is too long! Cards will be ugly! \033[0m" + answer.split("(")[
                          0] + " \033[91mHas length: " + str(
                    len(answer.split("(")[0])) + "/" + str(
                    2 * ANSWER_MAX_LINE_LENGTH) + "\033[0m"
                error_count = error_count + 1
                any_error_or_warning = True
            if len(answer.split("(")) > 1:
                if len("(" + answer.split("(")[1]) > ANSWER_MAX_LINE_LENGTH:  # if citation line is too long
                    print "\033[91mError: Citation of entry with ID: " + str(
                        answer_id) + " is too long! Cards will be ugly! \033[0m" + "(" + answer.split("(")[
                              1] + " \033[91mHas length: " + str(
                        len("(" + answer.split("(")[1])) + "/" + str(
                        ANSWER_MAX_LINE_LENGTH) + "\033[0m"
                    error_count = error_count + 1
                    any_error_or_warning = True
            if any_error_or_warning:
                print("")  # Organize Errors and Warnings in blocks grouped by id

        print "\033[1mAnswer-Report\n\033[0m\033[91m  Errors found: \033[0m\033[1m" + str(
            error_count) + "\n \033[0m\033[93m Warnings found: \033[0m\033[1m" + str(warning_count) + "\033[0m\n"
        return warning_count, error_count


def validate_categories():
    """
    Validates if any questions is applied to a valid category from the categories file
    :return: Warning and Error count
    """
    print "Validating category entries..."
    conn = create_connection("python_sqlite.db")
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id,question,category FROM qac ORDER BY id")
        error_count = 0
        warning_count = 0
        for entry in cur.fetchall():
            question_id = entry[0]
            category = entry[2]
            any_error_or_warning = False
            if category not in database_statistics.get_categories_from_file()[0]:
                any_error_or_warning = True
                error_count = error_count + 1
                print "\033[91mError: Category of entry with ID: " + str(
                    question_id) + " is missing a correct category \033[0m Current Category: " + category
            if any_error_or_warning:
                print("")  # Organize Errors and Warnings in blocks grouped by id

        print "\033[1mCategory-Report\n\033[0m\033[91m  Errors found: \033[0m\033[1m" + str(
            error_count) + "\n \033[0m\033[93m Warnings found: \033[0m\033[1m" + str(warning_count) + "\033[0m\n"
        return warning_count, error_count


if __name__ == '__main__':
    validate_questions()
    validate_answers()
    validate_categories()
