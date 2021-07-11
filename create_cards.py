import os
import re
import shutil
import sqlite3
from random import shuffle

from PIL import ImageFont, Image, ImageDraw

from constants import QUESTION_MAX_LINE_LENGTH, ANSWER_MAX_LINE_LENGTH, NEXT_QUESTION_Y_SKIP, SHUFFLE
from database_statistics import count_questions, get_categories_from_file


def create_connection(db_file):
    """
    Establishes a database connection
    :param db_file: File of the database
    :return: Successful connection
    """
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)


def split_lines(text, line_length):
    """
    Split a text in multiple lines at " " and returns the lines as list
    :param text: Text to be split
    :param line_length: Maximum length of each line
    :return: List with all lines
    """
    lines = []
    line_ends = [0]  # All line endings, first line has to start at index 0
    spaces = [m.start() for m in re.finditer(' ', text.strip(" "))]  # Find all spaces an write indexes to a list
    spaces.append(len(
        text))  # Append end of text to allow last line go to end of the last word, not the one before the last (the
    # last space)
    for i in range(1, int(len(text) / line_length) + 2):  # For how much lines there have to be
        line_ends.append(max([s for s in spaces if
                              s <= i * line_length]) + 1)  # Last space which index is less than
        # QUESTION_MAX_LINE_LENGTH
        lines.append(text[line_ends[i - 1]:line_ends[
            i]])  # Append line starting at last line_ends entry and going to line_ends[i]
    return lines


def get_questions_of_category(conn, category):
    """
    Gets all questions of a category from the database
    :param conn: Database connection
    :param category: Category of which questions will be retrieved
    :return: Set of all questions with the category
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM qac WHERE category=?", category)
    question_rows = cur.fetchall()
    if SHUFFLE:
        shuffle(question_rows)  # Shuffle questions, so that there is no order recognizable, otherwise ordered by id
    return question_rows  # could also use dict_factory, but indexes are ok here


def get_question_ids(conn):
    """
    Gets all ids of the questions in the database
    :param conn: Database connection
    :return: List of ids
    """
    cur = conn.cursor()
    cur.execute("SELECT id FROM qac")
    ids = [item[0] for item in cur.fetchall()]
    return ids


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
    with conn:  # Keep connection open, as long as necessary
        categories, categories_long = get_categories_from_file()  # get categories and long name
        card_count = 1

        question_database = {}
        for category in categories:
            question_database[category] = get_questions_of_category(conn,
                                                      category)  # Get all questions of those category from database before the loop because so they were just shuffled once
        while True:
            front = Image.open("assets/front.png")  # Load assets
            back = Image.open("assets/back.png")
            dv = ImageDraw.Draw(front)
            dh = ImageDraw.Draw(back)
            y = 100
            used_ids_for_current_card = []
            for category in categories:  # For each category
                print(category)
                questions = question_database[category]

                if (len(questions) == 0):  # if no new question was found
                    print("\nSuccessfully created " + str(card_count - 1) + " cards. Those can be found in ./out")
                    print(str(count_questions(conn) - 6 * (
                            card_count - 1)) + " Questions have been ignored. (Due to inapplicable categories)")
                    print("No more questions available to fill new card!")
                    print(
                        "Questions with the following id's were skipped: ")

                    used_ids = [item for item in used_ids if item not in used_ids_for_current_card]
                    used_ids.sort()
                    unused_used_cut = [item for item in get_question_ids(conn) if item not in used_ids]
                    for q_id in unused_used_cut:
                        print(q_id)
                    return  # End script - cards have been created

                for question_row in questions:  # question_row[ ] represents one question 0 - ID, 1 - question,
                    # 2 - answer, 3 - category
                    print(question_row)  # print full question_row
                    if (question_row[0] not in used_ids):  # if there is a not yet used question which have to be processed

                        used_ids.append(question_row[0])  # append to used list
                        used_ids_for_current_card.append(question_row[0])
                        question_database[category].remove(question_row)
                        question = question_row[
                            1].strip()  # Get question and remove possible whitespace after question mark
                        answer = question_row[2]  # Get answer of the question_row

                        question_lines = split_lines(question, QUESTION_MAX_LINE_LENGTH)
                        if len(question_lines) == 3:  # if question has to be split to multiple lines (here to 2 lines)
                            dv.text((220, y - 30), question_lines[0], font=fnt,
                                    fill=(0, 0, 0))  # Align all three lines to y
                            dv.text((220, y), question_lines[1], font=fnt, fill=(0, 0, 0))
                            dv.text((220, y + 30), question_lines[2], font=fnt, fill=(0, 0, 0))
                        elif len(question_lines) == 2:
                            dv.text((220, y - 15), question_lines[0], font=fnt,
                                    fill=(0, 0, 0))  # Align both lines with y in the middle
                            dv.text((220, y + 15), question_lines[1], font=fnt, fill=(0, 0, 0))
                        else:
                            dv.text((220, y), question_lines[0], font=fnt,
                                    fill=(0, 0, 0))  # Align the line in the middle (at y)

                        answer_lines = split_lines(answer.split("(")[0],
                                                   ANSWER_MAX_LINE_LENGTH)  # Max. 2 lines (because of answer checker
                        # in database_tools), Citation will be rendered in it's own line

                        citation_exists = False
                        if len(answer.split("(")) > 1:  # append citation if there is one
                            citation = answer.split("(")[1]
                            answer_lines.append(citation)
                            citation_exists = True
                        if len(answer_lines) == 3:  # if there are two lines and a citation
                            dh.text((620, y - 30), answer_lines[0], font=fnt,
                                    fill=(0, 0, 0))  # Align all three lines to y
                            dh.text((620, y), answer_lines[1], font=fnt, fill=(0, 0, 0))
                            dh.text((620, y + 30), "(" + answer_lines[2], font=fnt, fill=(0, 0, 0))
                        elif len(answer_lines) == 2:  # if there is just one line and a citation (a split was done)
                            dh.text((620, y - 15), answer_lines[0], font=fnt,
                                    fill=(0, 0, 0))  # Align the line a the citation to y
                            if citation_exists:  # 2nd line can be citation or just a second line
                                dh.text((620, y + 15), "(" + answer_lines[1], font=fnt, fill=(0, 0, 0))
                            else:
                                dh.text((620, y + 15), answer_lines[1], font=fnt, fill=(0, 0, 0))
                        else:  # if there is just a line
                            dh.text((620, y), answer_lines[0], font=fnt, fill=(0, 0, 0))  # Place the answer at y

                        y = y + NEXT_QUESTION_Y_SKIP  # go to the next question
                        break # a new question is added, break and continue with the next category

            front.save(
                "./out/front" + str(card_count) + ".png")  # save front and back of the card with texts written on it
            back.save("./out/back" + str(card_count) + ".png")
            card_count = card_count + 1


if __name__ == "__main__":
    create_cards()
