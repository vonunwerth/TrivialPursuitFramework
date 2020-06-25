# TODO different paper formats?! variable for x times x cards on same sheet
import os

from PIL import Image

Y_GAP = 0 # Glue both sides together without cutting the cards itself
X_GAP = 10

card = Image.open("assets/back.png")
sheet = Image.new('RGB', (card.width * 2 + (X_GAP * 1), card.height * 4 + (Y_GAP * 3)))

sheet_number = 1
for i in range(1, 5):  # ,(len([name for name in os.listdir('.') if os.path.isfile(name)])/2)):
    try:
        second_row_y = 0
        if i > 2:
            second_row_y = 2 * card.height
        print i
        front = Image.open("out/front" + str(i) + ".png")
        back = Image.open("out/back" + str(i) + ".png").rotate(180)
        print "Paste front of card " + str(i) + " on sheet" + str(sheet_number)
        sheet.paste(front, ((i - 1)%2 * card.width + (i - 1)%2 * X_GAP, 0 + second_row_y))
        print "Paste back of card " + str(i) + " on sheet" + str(sheet_number)
        sheet.paste(back, ((i - 1)%2 * card.width + (i - 1)%2 * X_GAP, card.height + Y_GAP + second_row_y))
    except:
        print "No more cards found"
        break

sheet.save("prints/print1.png")
