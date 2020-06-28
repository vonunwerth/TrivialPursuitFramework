# coding=utf-8
import codecs
import os  # Für jede Karte einen eigenen Ordner machen
from PIL import Image, ImageDraw, ImageFont

class Question:
    def __init__(self, question, answer, category):
        self.question = question
        self.answer = answer
        self.category = category


f = codecs.open("questions/questions.txt", "r", "utf-8")

fragen = []

question = ""
answer = ""
category = ""

qac_counter = 0
question_counter = 0
for x in f:
    if x.find("Q: ") >= 0:
        question = (x.split("Q: ")[1].split("\r\n")[0])  # Alles hinter Q:, alles vor  \r\n
        qac_counter = qac_counter + 1
    if x.find("A: ") >= 0:
        answer = (x.split("A: ")[1].split("\r\n")[0])
        qac_counter = qac_counter + 1
    if x.find("C: ") >= 0:
        category = (x.split("C: ")[1].split("\r\n")[0])
        qac_counter = qac_counter + 1
    if qac_counter == 3:
        fragen.append(Question(question, answer, category))
        qac_counter = 0
        question_counter = question_counter + 1


class Fragenkarte:
    def __init__(self, c_question = None, t_question = None, s_question = None, v_question = None, g_question = None, a_question = None,
                 c_answer = None, t_answer = None, s_answer = None, v_answer = None, g_answer = None, a_answer = None):
        self.c_question = c_question
        self.t_question = t_question
        self.s_question = s_question
        self.v_question = v_question
        self.g_question = g_question
        self.a_question = a_question
        self.c_answer = c_answer
        self.t_answer = t_answer
        self.s_answer = s_answer
        self.v_answer = v_answer
        self.g_answer = g_answer
        self.a_answer = a_answer


"""Charaktere = C
Technik = T
Spezies = S
Die Voyager = V
Geschichte, Politik, Kunst und Kultur und die Sternenflotte = G
Missionen = A"""
fragenkarten = []
f = Fragenkarte()
fragenkarten.append(f)

for frage in fragen:
    saved = False
    for fragekarte in fragenkarten:
        if frage.category == "C":
            if fragekarte.c_question is None:
                fragekarte.c_question = frage.question
                fragekarte.c_answer = frage.answer
                saved = True
                break
        if frage.category == "T":
            if fragekarte.t_question is None:
                fragekarte.t_question = frage.question
                fragekarte.t_answer = frage.answer
                saved = True
                break
        if frage.category == "S":
            if fragekarte.s_question is None:
                fragekarte.s_question = frage.question
                fragekarte.s_answer = frage.answer
                saved = True
                break
        if frage.category == "V":
            if fragekarte.v_question is None:
                fragekarte.v_question = frage.question
                fragekarte.v_answer = frage.answer
                saved = True
                break
        if frage.category == "G":
            if fragekarte.g_question is None:
                fragekarte.g_question = frage.question
                fragekarte.g_answer = frage.answer
                saved = True
                break
        if frage.category == "A":
            if fragekarte.a_question is None:
                fragekarte.a_question = frage.question
                fragekarte.a_answer = frage.answer
                saved = True
                break
    if not saved:
        f = Fragenkarte()
        if frage.category == "C":
            f.c_question = frage.question
            f.c_answer = frage.answer
        if frage.category == "S":
            f.s_question = frage.question
            f.s_answer = frage.answer
        if frage.category == "T":
            f.t_question = frage.question
            f.t_answer = frage.answer
        if frage.category == "V":
            f.v_question = frage.question
            f.v_answer = frage.answer
        if frage.category == "G":
            f.g_question = frage.question
            f.g_answer = frage.answer
        if frage.category == "A":
            f.a_question = frage.question
            f.a_answer = frage.answer
        fragenkarten.append(f)

fragenkarten.append(Fragenkarte())


fnt = ImageFont.truetype("arial.ttf", 25)

# Fragenkarten als Bilder erstellen
fragenkarte = 1
for fragekarte in fragenkarten:  # 6er Bündel aus Allen
    vorne = Image.open("assets/front.png")
    hinten = Image.open("assets/back.png")
    dv = ImageDraw.Draw(vorne)
    dh = ImageDraw.Draw(hinten)
    y = 100
    """for frage in fragen:
        zeile1 = frage
        zeile2 = ""
        if len(frage.question) > 60:
            zweizeilig = True
            zeile1 = frage.question[
                     0:60]  # TODO finde das letzte Leerzeichen oder - vor dem 60. Zeichen um Zeilenumbruch zu machen
            zeile2 = frage.question[60:len(frage.question)]
            dv.text((220, y - 15), zeile1, font=fnt, fill=(0, 0, 0))
            dv.text((220, y + 15), zeile2, font=fnt, fill=(0, 0, 0))
        else:
            dv.text((220, y), frage.question, font=fnt, fill=(0, 0, 0))

        # print frage.answer
        dh.text((620, y - 15), frage.answer.split("(")[0], font=fnt, fill=(0, 0, 0))
        dh.text((620, y + 15), "(" + frage.answer.split("(")[1], font=fnt, fill=(0, 0, 0))

        y = y + 103

    vorne.save("vorne" + str(fragenkarte) + ".png")
    hinten.save("hinten" + str(fragenkarte) + ".png")
    fragenkarte = fragenkarte + 1"""
