from enum import Enum


class QType(Enum):
    multiple_choice_question = 1
    true_false_question = 2
    short_answer_question = 3
    fill_in_multiple_blanks_question = 4
    text_only_question = 5
    multiple_answers_question = 6
    multiple_dropdowns_question = 7
    matching_question = 8
    numerical_question = 9
    calculated_question = 10
    essay_question = 11
    file_upload_question = 12


class Choice:

    def __init__(self, val, is_correct: bool, info=None, feedback=""):
        """Create a choice for a question"""
        self.val = val
        self.is_correct = is_correct
        self.feedback = feedback
        self.info = info


class Question:

    def __init__(self, title, question_type: QType, question_choices: [Choice] = [], point=1):
        self.title = title
        self.point = point
        self.type = question_type
        self.choices = question_choices

