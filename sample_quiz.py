from Quiz import *
from Question import *

if __name__ == '__main__':
    q1c1 = Choice(106, False)
    q1c2 = Choice(206, True)
    q1c3 = Choice(156, False)
    q1c4 = Choice(256, False)

    q2c1 = Choice(32, True, 0)  # info refers to the +- value

    q3c1 = Choice(False, False)
    q3c2 = Choice(True, True)

    q4c1 = Choice("berlin", True)
    q4c2 = Choice("Berlin", True)

    q5c1 = Choice("paris", True, 1)  # info refers to the blank no.
    q5c2 = Choice("Paris", True, 1)
    q5c3 = Choice("rome", True, 2)
    q5c4 = Choice("Rome", True, 2)

    q6c1 = Choice("Cape Town", True)
    q6c2 = Choice("Pretoria", True)
    q6c3 = Choice("Bloemfontein", True)
    q6c4 = Choice("Johannesburg", False)

    q7c1 = Choice("Hair", True, 1)  # info refers to the dropdown no.
    q7c2 = Choice("Eyes", False, 1)
    q7c3 = Choice("Slower", False, 2)
    q7c4 = Choice("Faster", True, 2)

    q10c1 = Choice("slow", True, 1)  # info refers to the match no.
    q10c2 = Choice("fast", True, 1)
    q10c3 = Choice("big", True, 2)
    q10c4 = Choice("small", True, 2)

    q1 = Question("How many bones in the human body?", QType.multiple_choice_question, [q1c1, q1c2, q1c3, q1c4])
    q2 = Question("How many teeth in adult human mouth?", QType.numerical_question, [q2c1])
    q3 = Question("A human's thumb is as long as his or her nose?", QType.true_false_question, [q3c1, q3c2])
    q4 = Question("What is the capital of germany?", QType.short_answer_question, [q4c1, q4c2])
    q5 = Question("The capital of France is [1] and the capital of Italy is [2]?",
                  QType.fill_in_multiple_blanks_question, [q5c1, q5c2, q5c3, q5c4])
    q6 = Question("What are the capitals of South Africa?",
                  QType.multiple_answers_question, [q6c1, q6c2, q6c3, q6c4])
    q7 = Question("Cells related to [1] divide remarkably [2] than other cells in the body.",
                  QType.multiple_dropdowns_question, [q7c1, q7c2, q7c3, q7c4])
    q8 = Question("Upload the drawing of the human lungs here", QType.file_upload_question, [])
    q9 = Question("You can do it! Don't give up", QType.text_only_question, [])
    q10 = Question("Match the following", QType.matching_question, [q10c1, q10c2, q10c3, q10c4])
    q11 = Question("Write an essay on how to cheat during exams", QType.essay_question, [])

    g1 = Group(2, [q1, q2, q3])
    g2 = Group(2, [q4, q5, q6])
    g3 = Group(1, [q7])
    g4 = Group(2, [q8, q9])
    g5 = Group(2, [q10, q11])

    quiz = Quiz("The master quiz", "You need 100% marks in this quiz to pass this course :(", [g1, g2, g3, g4, g5])

    print(quiz)