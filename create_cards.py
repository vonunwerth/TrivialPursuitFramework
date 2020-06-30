import os
import re
import shutil
import sqlite3

from PIL import ImageFont, Image, ImageDraw

from constants import QUESTION_MAX_LINE_LENGTH
from database_statistics import count_questions, get_categories_from_file


def create_connection(db_file):
    """
    Establishes a database connection
    :param db_file: File of the database
    :return: Successfull connection
    """
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)


def get_questions_of_categoriy(conn, category):
    """
    Gets all questions of a category from the database
    :param conn: Database connection
    :param category: Category of which questions will be retrieved
    :return: Set of all questions with the category
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM qac WHERE category=?", category)
    return cur.fetchall()  # Could also use dict_factory


def create_cards():
    """
    Creates question cards filled with the questions provided by the database
    :return: Returns when no new card can be created
    """
    if os.path.exists("out") and os.path.isdir("out"):
        shutil.rmtree('out')  # Clean out folder
    os.mkdir("out")  # create new out folder for result cards
    conn = create_connection("python_sqlite.db")  # If not exist, create database, else establish a connection
    used_ids = []
    fnt = ImageFont.truetype("arial.ttf", 25)
    with conn:
        categories, categories_long = get_categories_from_file()
        # TODO Write categories on blank front, back
        card_count = 1
        while True:
            vorne = Image.open("assets/front_cat.png")
            hinten = Image.open("assets/back_cat.png")
            dv = ImageDraw.Draw(vorne)
            dh = ImageDraw.Draw(hinten)
            y = 100
            for category in categories:
                print category
                questions = get_questions_of_categoriy(conn, category)  # TODO Mischen
                for question_row in questions:  # question_row[ ] 0 - ID, 1 - question, 2 - answer, 3 - category
                    print question_row
                    if (question_row[0] in used_ids) and (questions.index(question_row) == (len(questions) - 1)):
                        print "\nSuccessfully created " + str(card_count - 1) + " cards. Those can be found in ./out"
                        print str(count_questions(conn) - 6 * (
                                card_count - 1)) + " Questions have been ignored. (Due to inapplicable categories)"
                        print "No more questions available to fill new card!"  # TODO Druckgroesse
                        return  # End scipt - cards have been created
                    if question_row[0] not in used_ids:
                        used_ids.append(question_row[0])
                        question = question_row[
                            1].strip()  # Get question and remove possible whitespace after questionsmark
                        answer = question_row[2]
                        if len(question) > QUESTION_MAX_LINE_LENGTH:
                            spaces = [m.start() for m in re.finditer(' ', question.strip(" "))]  # Find all spaces
                            print spaces
                            line1_end = max(
                                [s for s in spaces if s <= QUESTION_MAX_LINE_LENGTH]) + 1  # Last space which index is less than 60
                            print line1_end
                            line1 = question[0:line1_end]  # Zeilenumbruch zu machen, ggf sogar 3 Zeilen machen
                            line2 = question[line1_end:len(question)]
                            dv.text((220, y - 15), line1, font=fnt, fill=(0, 0, 0))
                            dv.text((220, y + 15), line2, font=fnt, fill=(0, 0, 0))
                        else:
                            dv.text((220, y), question, font=fnt, fill=(0, 0, 0))
                        # print frage.answer
                        if len(answer.split("(")) > 1:  # TODO Zu lange Antowrten --> wenigstens Warning ausgeben
                            dh.text((620, y - 15), answer.split("(")[0], font=fnt, fill=(0, 0, 0))
                            dh.text((620, y + 15), "(" + answer.split("(")[1], font=fnt, fill=(0, 0, 0))
                        else:
                            dh.text((620, y), answer, font=fnt, fill=(0, 0, 0))
                        y = y + 103
                        break

            vorne.save("./out/front" + str(card_count) + ".png")
            hinten.save("./out/back" + str(card_count) + ".png")
            card_count = card_count + 1


if __name__ == "__main__":
    create_cards()
