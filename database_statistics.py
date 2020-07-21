import codecs
import sqlite3


def create_connection(db_file):
    """
    Create a database connection to a SQLite database
    :param db_file: SQLite file containing the database
    :return: Connection
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except sqlite3.Error as e:
        print(e)


def count_categories(conn, category):
    """
    Count questions of the given category
    :param conn: Connection to the database
    :param category: Wished category
    :return: Count of questions of category
    """
    cur = conn.cursor()
    cur.execute("SELECT COUNT(id) FROM qac WHERE category=?", category)
    return cur.fetchall()


def count_questions(conn):
    """
    Count all questions
    :param conn: Connection to the database
    :return: Just the number of all questions
    """
    cur = conn.cursor()
    cur.execute("SELECT COUNT(id) FROM qac")
    return cur.fetchall()[0][0]


def get_categories_from_file():
    """
    Reads the category string from the categories.txt file
    :return: Tupel (Categories one letter, Category long name)
    """
    cat = []
    cat_long = []
    f = codecs.open("questions/categories.txt", "r", "utf-8")
    for line in f:
        cat.append(line.split(":")[0].strip())
        cat_long.append(line.split(":")[1].strip())
    return cat, cat_long


def database_statistics():
    """
    Generates interesting statistics about questions count, database entries, ...
    :return: Successfull execution
    """
    conn = create_connection("python_sqlite.db")
    categories, categories_long = get_categories_from_file()
    with conn:
        numbers = []
        for category in categories:
            rows = count_categories(conn, category)
            for row in rows:
                for number in row:
                    numbers.append(number)
                    print "There are " + str(number) + " questions of category " + categories_long[
                        categories.index(category)]
        print "\n" + str(min(numbers)) + " complete question cards can be created.."
        print "It exist " + str(count_questions(conn)) + " Questions."
        print str(count_questions(conn) - 6 * (
            min(numbers))) + " Questions will be ignored. (Due to inapplicable categories)"


if __name__ == '__main__':
    database_statistics()
