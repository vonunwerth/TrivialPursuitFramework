# TODO Cleanup database, manual unique check, etc.
# TODO check if every question ends with a question mark
# TODO Check length of questions and answer is not to long
# TODO Check each Question has valid category
# TODO function which can repair corrupted entries
import sqlite3


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
        for entry in cur.fetchall():
            question_id = entry[0]
            question = entry[1]
            if len(question) > 60:
                print "\033[91mError: ID: " + str(question_id) + " is to long! \033[0m" + question
            if question[-1] != "?":
                if question[-1] == " ":
                    print "\033[93mWarning: ID: " + str(
                        question_id) + " has spaces attached to the back. \033[0m" + question
                else:
                    print "\033[93mWarning: ID: " + str(question_id) + " has not a ? as last symbol! \033[0m" + question
            print("\n")


if __name__ == '__main__':
    validate_questions()
