from Question import Question
from typing import List


class Group:

    def __init__(self, selected: int = 1, questions: List[Question] = [], is_user_created=True):
        """Create a group"""
        self.selected = selected
        self.is_user_created = is_user_created
        self.questions = questions


class Quiz:

    def __init__(self, title: str, description: str, groups: List[Group] = []):
        """Create a quiz"""
        self.title = title
        self.description = description
        self.groups = groups