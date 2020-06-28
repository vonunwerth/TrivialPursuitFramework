import sqlite3


# https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except sqlite3.Error as e:
        print(e)


def count_categories(category):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(id) FROM qac WHERE category=?", (category))
    return cur.fetchall()


def count_questions():
    cur = conn.cursor()
    cur.execute("SELECT COUNT(id) FROM qac")
    return cur.fetchall()[0][0]

conn = create_connection("pythonsqlite.db")
categories = ["C", "S", "T", "V", "G", "M"]  # TODO read from category file
categories_long = ["Charaktere", "Spezies", "Trivia", "Die Voyager", "Geschichte", "Missionen"]
with conn:
    numbers = []
    for category in categories:
        rows = count_categories(category)
        for row in rows:
            for number in row:
                numbers.append(number)
                print "Es existieren " + str(number) + " Fragen zur Kategorie " + categories_long[
                    categories.index(category)]
    print "\nDamit koennen " + str(min(numbers)) + " vollstaendige Fragenkarten erstellt werden."
    print "Insgesamt existieren " + str(count_questions()) + " Fragen."
