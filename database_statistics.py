import codecs
import sqlite3


# https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except sqlite3.Error as e:
        print(e)


def count_categories(conn, category):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(id) FROM qac WHERE category=?", category)
    return cur.fetchall()


def count_questions(conn):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(id) FROM qac")
    return cur.fetchall()[0][0]


def get_categories_from_file():
    cat = []
    cat_long = []
    f = codecs.open("questions/categories.txt", "r", "utf-8")
    for line in f:
        cat.append(line.split(":")[0].strip())
        cat_long.append(line.split(":")[1].strip())
    return cat, cat_long


def database_statistics():
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
