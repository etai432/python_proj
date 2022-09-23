import random


def main():
    words = {'להקל על, לשכך': 'alleviate', 'הקשר, קונטקסט': 'context', 'קטע קריאה': 'passage', 'ביטוי': 'phrase',
             'עדינות, שנינות': 'subtlety', 'להעריך, לאמוד': 'assess', 'לא מדוייק': 'inaccurate',
             'שווה ערך': 'equivalent', 'באופן הולם, בצורה נאותה': 'appropriately', 'להתקין': 'install',
             'תוכנת מחשב': 'software', 'מעודן, דק, שנון, מתוחכם': 'subtle', 'מגרעת, חיסרון': 'drawback',
             'באופן בלתי הולם': 'inappropriately', 'מקצועי, מיומן': 'proficient', 'כמות מספקת, מספיק': 'sufficient',
             'מיותר, עודף': 'superfluous', 'מדוייק, דייקן': 'accurate'}  # hebrew : english
    correct = 0
    errors = 0
    length = len(words)
    while correct != length:
        start = correct
        picked = []
        for i in range(len(words)):
            pick = random.choice(list(words.keys()))
            while pick in picked:
                pick = random.choice(list(words.keys()))
            picked.append(pick)
            answer = input(str(pick) + " ")
            if answer == words[pick]:
                print("correct")
                correct += 1
                words.pop(pick)
            else:
                print("the correct answer was: " + words[pick])
                errors += 1
        print("you got " + str(correct - start) + " words this round, " + str(length - correct) + " left!")
    print("you had " + str(errors) + " errors")


if __name__ == '__main__':
    main()
