# TODO different paper formats?! variable for x times x cards on same sheet
from PIL import Image


def print_cards():
    y_gap = 0  # Glue both sides together without cutting the cards itself
    x_gap = 10

    sheet_number = 1
    while True:
        print "Creating sheet number " + str(sheet_number)
        card = Image.open("assets/back.png")
        sheet = Image.new('RGB', (card.width * 2 + (x_gap * 1), card.height * 4 + (y_gap * 3)))
        for i in range(1, 5):  # ,(len([name for name in os.listdir('.') if os.path.isfile(name)])/2)):
            try:
                second_row_y = 0
                if i > 2:
                    second_row_y = 2 * card.height
                front = Image.open("out/front" + str(i + (sheet_number - 1) * 4) + ".png")
                back = Image.open("out/back" + str(i + (sheet_number - 1) * 4) + ".png").rotate(180)
                print "Paste front of card " + str(i + (sheet_number - 1) * 4) + " on sheet" + str(sheet_number)
                sheet.paste(front, ((i - 1) % 2 * card.width + (i - 1) % 2 * x_gap, 0 + second_row_y))
                print "Paste back of card " + str(i + (sheet_number - 1) * 4) + " on sheet" + str(sheet_number)
                sheet.paste(back, ((i - 1) % 2 * card.width + (i - 1) % 2 * x_gap, card.height + y_gap + second_row_y))
            except IOError:
                print "No more cards found"
                sheet.save("prints/print" + str(sheet_number) + ".png")
                return
        sheet.save("prints/print" + str(sheet_number) + ".png")
        sheet_number = sheet_number + 1


if __name__ == '__main__':
    print_cards()
