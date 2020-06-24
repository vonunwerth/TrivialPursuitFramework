import sqlite3

from PIL import ImageFont, Image, ImageDraw

from database_statistics import count_questions


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except sqlite3.Error as e:
        print(e)


def get_questions_of_categoriy(category):
    cur = conn.cursor()
    cur.execute("SELECT * FROM qac WHERE category=?", (category))
    return cur.fetchall() # Could also use dict_factory


conn = create_connection("pythonsqlite.db")
used_ids = []
fnt = ImageFont.truetype("arial.ttf", 25)
with conn:
    categories = ["C", "S", "T", "V", "G", "M"]  # TODO read from category file

    card_count = 1
    while (True):
        vorne = Image.open("./assets/vorne.png")
        hinten = Image.open("./assets/hinten.png")
        dv = ImageDraw.Draw(vorne)
        dh = ImageDraw.Draw(hinten)
        y = 100
        for category in categories:
            print category
            questions = get_questions_of_categoriy(category)
            for question_row in questions: # question_row[ ] 0 - ID, 1 - question, 2 - answer, 3 - category
                print question_row
                if (question_row[0] in used_ids) and (questions.index(question_row) == (len(questions) - 1)):
                    print "\nSuccessfully created " + str(card_count - 1) + " cards. Those can be found in ./out"
                    print str(count_questions() - 6 * (card_count - 1)) + " Questions have been ignored. (Due to inapplicable categories)"
                    print "No more questions available to fill new card!" # TODO Druckgroesse
                    exit(-1)
                if question_row[0] not in used_ids:
                    used_ids.append(question_row[0])
                    question = question_row[1]
                    answer = question_row[2]
                    line1 = question
                    line2 = ""
                    if len(question) > 60:
                        line1 = question[0:60]  # TODO finde das letzte Leerzeichen oder - vor dem 60. Zeichen um Zeilenumbruch zu machen, ggf sogar 3 Zeilen machen
                        line2 = question[60:len(question)]
                        dv.text((220, y - 15), line1, font=fnt, fill=(0, 0, 0)) #TODO geht noch nicht!
                        dv.text((220, y + 15), line2, font=fnt, fill=(0, 0, 0))
                    else:
                        dv.text((220, y), question, font=fnt, fill=(0, 0, 0))
                    # print frage.answer
                    if (len(answer.split("(")) > 1): # TODO Zu lange Antowrten --> wenigstens Warning ausgeben
                        dh.text((620, y - 15), answer.split("(")[0], font=fnt, fill=(0, 0, 0))
                        dh.text((620, y + 15), "(" + answer.split("(")[1], font=fnt, fill=(0, 0, 0))
                    else:
                        dh.text((620, y), answer, font=fnt, fill=(0, 0, 0))
                    y = y + 103
                    break

        vorne.save("./out/vorne" + str(card_count) + ".png")
        hinten.save("./out/hinten" + str(card_count) + ".png")
        card_count = card_count + 1