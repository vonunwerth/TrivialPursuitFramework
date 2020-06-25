# TODO different paper formats?! variable for x times x cards on same sheet
import os

from PIL import Image

Y_GAP = 0 # Glue both sides together without cutting the cards itself
X_GAP = 10

card = Image.open("assets/back.png")
sheet = Image.new('RGB', (card.width * 2 + (X_GAP * 1), card.height * 4 + (Y_GAP * 3)))

for i in range(1, 4):  # ,(len([name for name in os.listdir('.') if os.path.isfile(name)])/2)):
    front = Image.open("out/front" + str(i) + ".png")
    back = Image.open("out/back" + str(i) + ".png").rotate(180)
    sheet.paste(front, ((i - 1) * card.width + (i - 1) * X_GAP, 0))
    sheet.paste(back, ((i - 1) * card.width + (i - 1) * X_GAP, card.height + Y_GAP))

sheet.save("prints/print1.png")
