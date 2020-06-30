# TODO Cleanup database, manual unique check, etc.
# TODO check if every question ends with a question mark
# TODO Check length of questions and answer is not to long
# TODO Check each Question has valid category
# TODO function which can repair corrupted entries
import sqlite3

import database_statistics


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except sqlite3.Error as e:
        print(e)


def validate_questions():
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
            any_error = False
            if len(question) > 120:
                print "\033[91mError: Question of entry with ID: " + str(question_id) + " is to long! Cards will be ugly! \033[0m" + question
                error_count = error_count + 1
                any_error = True
            if question[-1] != "?":
                any_error = True
                warning_count = warning_count + 1
                if question[-1] == " ":
                    print "\033[93mWarning: Question of entry with ID: " + str(
                        question_id) + " has spaces attached to the back. \033[0m" + question
                else:
                    print "\033[93mWarning: Question of entry with ID: " + str(question_id) + " has not a ? as last symbol! \033[0m" + question
            if any_error:
                print("")  # Organize Errors and Warnings in blocks grouped by id

        print "\033[1mQuestion-Report\n\033[0m\033[91m  Errors found: \033[0m\033[1m" + str(
            error_count) + "\n \033[0m\033[93m Warnings found: \033[0m\033[1m" + str(warning_count) + "\033[0m\n"
        return (warning_count, error_count)


def validate_answers():
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
            answer_cat = entry[2]
            any_error = False
            if len(answer.split("(")[0]) > 60:
                print "\033[91mError: Answer of entry with ID: " + str(answer_id) + " is to long! Cards will be ugly! \033[0m" + answer
                error_count = error_count + 1
                any_error = True
            if answer_cat != "T" and (
                    answer.find("(") < 0 or answer.find(")") < 0):  # TODO just for this Star Trek thingy thing
                any_error = True
                warning_count = warning_count + 1
                print "\033[93mWarning: Answer of entry with ID: " + str(
                    answer_id) + " is missing correct citation and is not of category: Trivia \033[0m" + answer  # TODO not everyone will use citations!
            if any_error:
                print("")  # Organize Errors and Warnings in blocks grouped by id

        print "\033[1mAnswer-Report\n\033[0m\033[91m  Errors found: \033[0m\033[1m" + str(
            error_count) + "\n \033[0m\033[93m Warnings found: \033[0m\033[1m" + str(warning_count) + "\033[0m\n"
        return (warning_count, error_count)


def validate_categories():
    print "Validating category entries..."
    conn = create_connection("python_sqlite.db")
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id,question,category FROM qac ORDER BY id")
        error_count = 0
        warning_count = 0
        for entry in cur.fetchall():
            question_id = entry[0]
            question = entry[1]
            category = entry[2]
            any_error = False
            if category not in database_statistics.get_categories_from_file()[0]:
                any_error = True
                error_count = error_count + 1
                print "\033[91mError: Category of entry with ID: " + str(
                    question_id) + " is missing a correct category \033[0m Current Category: " + category
            if any_error:
                print("")  # Organize Errors and Warnings in blocks grouped by id

        print "\033[1mCategory-Report\n\033[0m\033[91m  Errors found: \033[0m\033[1m" + str(
            error_count) + "\n \033[0m\033[93m Warnings found: \033[0m\033[1m" + str(warning_count) + "\033[0m\n"
        return (warning_count, error_count)


if __name__ == '__main__':
    validate_questions()
    validate_answers()
    validate_categories()
