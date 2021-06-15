from Question import Question
question_prompts = [
    'Ile paskow ma logo Adidas?\n (a) 1\n (b) 2\n (c) 3\n\n',
    'Jaka substancje zawiera Yerba?\n (a) mateine\n (b) kofeine\n (c) teine\n\n',
    'Jaki jest jedyny sluszny majonez?\n (a) Kielecki\n (b) Winiary\n (c) Develey\n\n'
]

questions = [
    Question(question_prompts[0], "c"),
    Question(question_prompts[1], "a"),
    Question(question_prompts[2], "b")
]

def run_test(questions):
    score = 0
    for question in questions:
        answer = input(question.prompt)
        if answer == question.answer:
            score += 1
    print("Zdobyłeś" + str(score) + "/" + str(len(questions)) + "punkty")

run_test(questions)

