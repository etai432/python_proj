import random


def main():
    words = {'אוטונומיה':'autonomy', 'להיות מודע ל':'be conscious of', 'התנהגות':'conduct', 'התפתחות':'development', 'להתנסות':'To Experiment',
    'מבוגר':'grown-up', 'יד ביד':'Hand in hand', 'מנהיגות':'Leadership', 'תערוכה':'Exhibition', 'עמית':'peer', 'אחראי':'responsible', 
    'נטייה':'Tendency', 'לקשר':'Associate', 'להגביר':'boost', 'ברור':'evident', 'להדגים':'illustrate', 'להוביל ל':'lead to', 
    'תוצאה':'outcome', 'ביטחון עצמי':'Self confidence', 'לערער':'appeal', 'להציג':'exhibit', 'בידוד':'Isolation', 
    'הדדי, משותף':'Mutual', 'יקר ערך':'precious', 'לנצל':'Exploit', 'ליישם':'implement', 'לחזות':'predict', 'צפוי':'predictible', 
    'להכשיר':'qualify', 'הכשרה':'qualification'}  # hebrew : english
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
    #test

if __name__ == '__main__':
    main()
