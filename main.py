# This is a sample Python script.
import time
import re
import pyautogui
from PIL import ImageOps
import pytesseract as pt
import winsound


def extract(ressources):
    strip1 = ImageOps.expand(ressources.crop((0, 0, 160, 40)), 2, )
    strip2 = ImageOps.expand(ressources.crop((0, 40, 160, 90)), 2, )
    strip3 = ImageOps.expand(ressources.crop((0, 90, 160, 130)), 2, )
    pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    return (''.join(re.findall(r'\d+', pt.image_to_string(strip1))),
            ''.join(re.findall(r'\d+', pt.image_to_string(strip2))),
            ''.join(re.findall(r'\d+', pt.image_to_string(strip3))))


def grab_resources():
    s = pyautogui.screenshot(region=(80, 120, 160, 130))
    s = s.convert('L')
    s = s.point(lambda p: 0 if p > 220 else 255)
    return s


def click_to(x, y, dur=0.5, t=0):
    if t > 0:
        print("look for the village number " + str(t) + '\n')
    pyautogui.moveTo(x, y, dur)
    pyautogui.click()


def print_resources(gold, pink, dark, isInt):
    if isInt:
        print(f" - gold : {'{:,}'.format(gold).replace(',', ' ')} \n"
              f" - pink : {'{:,}'.format(pink).replace(',', ' ')} \n"
              f" - dark : {'{:,}'.format(dark).replace(',', ' ')} \n")
    else:
        print(f" - gold : {gold} \n - pink : {pink} \n - dark : {dark} \n ")


def next_village(c):
    time.sleep(2)
    click_to(1763, 824, 0.1, c)


def launch_attack():
    click_to(153, 972)
    click_to(1265, 660, 0.5, 1)


def enough_resources(gold, pink, dark):
    return gold > 1000000 or pink > 1000000 or (gold > 800000 and pink > 800000)


def main():
    resource_value_not_found_counter = 0
    already_missed_some = False
    launch_attack()
    village_count = 2
    while True:
        time.sleep(3)
        ressources = grab_resources()
        ressources.show()
        gold, pink, dark = extract(ressources)

        if all(len(var) == 0 for var in (gold, pink, dark)):
            print("Values not found")
            if resource_value_not_found_counter > 4:
                print()
                next_village(village_count)
                village_count += 1
                resource_value_not_found_counter = 0
            else:
                print("Retrying... \n")
                resource_value_not_found_counter += 1
            already_missed_some = False
            continue

        elif any(len(var) == 0 for var in (gold, pink, dark)):
            print("Values extraction failed : \n")
            print_resources(gold, pink, dark, False)
            if not already_missed_some:
                already_missed_some = True
                print("Retrying... \n")
                continue
            resource_value_not_found_counter = 0
            already_missed_some = False
            next_village(village_count)
            village_count += 1

        else:
            resource_value_not_found_counter = 0
            already_missed_some = False
            gold, pink, dark = int(gold), int(pink), int(dark)
            if dark > 20000 or gold > 2000000 or pink > 2000000:
                print("Values extraction failed : \n")
                print_resources(gold, pink, dark, True)
                next_village(village_count)
                village_count += 1

            elif enough_resources(gold, pink, dark):
                winsound.Beep(2000, 200)
                print("Village found ! \n")
                print_resources(gold, pink, dark, True)
                print("Programm shutting down")
                return
            else:
                print("Not enough resources : \n")
                print_resources(gold, pink, dark, True)
                next_village(village_count)
                village_count += 1


if __name__ == '__main__':
    try:
        time.sleep(2)
        main()

    except KeyboardInterrupt:
        print("\nProgram stopped.")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
