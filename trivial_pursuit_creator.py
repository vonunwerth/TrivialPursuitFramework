import database_statistics as dbs
import questions_to_database as qtb
import create_cards as cc
import print_cards as pc

print "This software will create printable questions sheets for Trivial Pursuit."
print "The questions are taken from a questions.txt file from the folder questions."
print "Please specify also the categories in a file called categories.txt in the same folder."
raw_input("Press \033[1mENTER\033[0m to start adding new questions from ./questions/questions.txt to the database.\n"
          "Already inserted questions will be ignored (The questions text must be unique.)")

qtb.questions_to_database()
raw_input("Press \033[1mENTER\033[0m to continue and show available statistics on how much cards can be created.")
dbs.database_statistics()
raw_input("Press \033[1mENTER\033[0m to create questions cards (front and back) in the ./out folder")
cc.create_cards()
raw_input(
    "Press \033[1mENTER\033[0m to create printable sheets with 4 questions card, which can be cut, kinked and glued "
    "together.")
pc.print_cards()
print "Congratulations. You can find the result in ./prints."
