import string
import random
import os
import uuid
import sys
import shutil
from zipfile import ZipFile
from io import StringIO
import sympy as sy
from mistletoe import Document
from mistletoe.html_renderer import HTMLRenderer
import xml.etree.ElementTree as ET
from datetime import date
from typing import List


class Qtype:
    """
    Validate and convert question type
    """
    qtypes = {
        'multiple choice': 1,
        'multiple answers': 2,
        'numerical': 3,
        'formula': 4,
        'essay': 5,
        'blank': 6,
        'multiple blanks': 7,
        'matching': 8,
        'multiple dropdown': 9,
        'file': 10,
        'text': 11
    }

    @classmethod
    def getQtype(self, qtype):
        if qtype.lower() in self.qtypes:
            return self.qtypes[qtype.lower()]
        return -1


class Choice:

    def __init__(self, val, is_correct: bool, ident="", feedback=""):
        """Create a choice for a question"""
        self.val = val
        self.is_correct = is_correct
        self.feedback = feedback
        self.ident = ident

    def setVal(self, doc):
        for item in doc.children:
            if item.__class__.__name__ == 'RawText':
                self.val += item.content
            elif item.__class__.__name__ == 'LineBreak':
                self.val += '\n'

    def setKey(self, doc):
        for item in doc.children:
            if item.__class__.__name__ == 'RawText':
                self.key += item.content
            elif item.__class__.__name__ == 'LineBreak':
                self.key += '\n'

    def setId(self, ident):
        self.ident = ident

    def setFeedback(self, li):
        for fb in li.children:
            if fb.__class__.__name__ == 'Setting' and fb.option == 'feedback':
                self.feedback += fb.content + '\n'
            else:
                raise Exception('Unexpected item found.')


class MultipleChoice(Choice):
    """
    Answer choice for Multiple choice, Multiple answers
    """

    def __init__(self, doc, renderer=HTMLRenderer):
        """
        Create a new choice from parsed MD data
        Raises an error if any issue found
        """
        super().__init__('', False, '', '')

        if doc.leader != '*':
            raise Exception('\'*\' is required for answer choices.')
        for item in doc.children:
            if item.__class__.__name__ == 'Paragraph':
                self.setVal(item)
            elif item.__class__.__name__ == 'Quote':
                self.is_correct = True
                self.setVal(item.children[0])
            elif item.__class__.__name__ == 'List':
                for li in item.children:
                    self.setFeedback(li)
        with renderer() as renderer:
            self.feedback = renderer.render(Document(self.feedback))

    def debug(self):
        print('  val:', self.val)
        print('  is_correct:', self.is_correct)
        print('  ident:', self.ident)
        print('  feedback:', self.feedback)


class Numerical(Choice):
    """
    Answer for Numerical
    """

    def __init__(self, doc):
        """
        Create a new choice from parsed MD data
        Raises an error if any issue found
        """
        super().__init__(0.0, False, '', '')
        self.margin = 0.0

        for item in doc.children:
            if item.__class__.__name__ == 'Paragraph':
                split = item.children[0].content.split(',')
                self.val = float(split[0])
                self.margin = float(split[1])
            else:
                raise Exception('Answer format is incorrect')

    def debug(self):
        print('  val:', self.val)
        print('  margin:', self.margin)
        print('  ident:', self.ident)


class Formula(Choice):
    """
    Answer for Formula
    """

    def __init__(self):
        """
        Create a new choice from parsed MD data
        Raises  an error if any issue found
        """
        super().__init__(0, True, '', '')
        self.vars = []
        self.formula = ''
        self.margin = ''
        self.generatedValues = []

    def setVar(self, doc):
        """
        Set variables
        """
        text = doc.children[0]
        if text.__class__.__name__ != 'Paragraph':
            raise Exception('Answer format is incorrect')
        self.vars.append([x.strip() for x in text.children[0].content.split(',')])

    def setFormula(self, doc):
        text = doc.children[0]
        if text.__class__.__name__ != 'Paragraph':
            raise Exception('Answer format is incorrect')
        self.formula = text.children[0].content

    def setAnswer(self, doc):
        if doc.__class__.__name__ != 'Paragraph':
            raise Exception('Answer format is incorrect')
        split = [x.strip() for x in doc.children[0].content.split(',')]
        self.val = int(split[0])
        self.margin = int(split[1].strip('%'))
        self.generateValues()

    def generateValues(self):
        alphabet_string = string.ascii_uppercase
        alphabet_list = list(alphabet_string)
        for i in range(self.val):
            tmpList = []
            for var in self.vars:
                # Get a random number from given min and max range
                randNum = round(random.uniform(float(var[1]), float(var[2])), int(var[3]))
                # Get variable and assign its value as randNum
                tmp = (var[0], randNum)
                tmpList.append(tmp)
            # Generate solution with given formula. Functions similarly to eval
            expr = sy.sympify(self.formula)
            solution = round(expr.subs(tmpList), int(var[3]))
            tmpList.append((alphabet_list[i], solution))
            self.generatedValues.append(tmpList)

    def debug(self):
        print('  vars:', self.vars)
        print('  formula:', self.formula)
        print('  val:', self.val)
        print('  margin:', self.margin)
        print('  generatedValues:', self.generatedValues)


class Matching(Choice):
    """
    Answer choice for Matching, Multiple Blanks, Multiple Dropdown
    """

    def __init__(self, doc, key, renderer=HTMLRenderer):
        """
        Create a new choice from parsed MD data
        Raises an error if any issue found
        """
        super().__init__('', False, '', '')
        self.key = ''

        if key.__class__.__name__ == 'Paragraph':
            self.setKey(key)
        else:
            raise Exception('Key format is incorrect for matching???')
        if doc.leader != '*':
            raise Exception('\'*\' is required for answer choices.')
        for item in doc.children:
            if item.__class__.__name__ == 'Paragraph':
                self.setVal(item)
            elif item.__class__.__name__ == 'Quote':
                self.is_correct = True
                self.setVal(item.children[0])
            elif item.__class__.__name__ == 'List':
                for li in item.children:
                    self.setFeedback(li)
        with renderer() as renderer:
            self.feedback = renderer.render(Document(self.feedback))

    def debug(self):
        print('  key:', self.key)
        print('  val:', self.val)
        print('  is_correct:', self.is_correct)
        print('  ident:', self.ident)
        print('  feedback:', self.feedback)


class Question:

    def __init__(self, title, ident, question_type=1, question_choices: [Choice] = [], points=1):
        self.title = title
        self.ident = ident
        self.points = points
        self.type = question_type
        self.choices = question_choices


class Group:

    def __init__(self, selected: int = 1, questions: List[Question] = [], is_user_created=True):
        """Create a group"""
        self.selected = selected
        self.is_user_created = is_user_created
        self.questions = questions


class Quiz:

    def __init__(self, title: str, description: str, ident: str, groups: List[Group] = []):
        """Create a quiz"""
        self.title = title
        self.description = description
        self.ident = ident
        self.groups = groups

    def print(self):
        for group in self.groups:
            for question in group.questions:
                print(question)
        return


class ParsedQuestion(Question):
    """
	Information of each question

	Attr:
		title (str): Question title
		ident (str): Question unique identifier
		points (int): Question points
		question (str): Question instruction. escaped-html format
		answers (List[any]): Question answers. Format follows the question type
		keys (List(str)): Keys for Multiple Blank answers
		qtype (str): Question type
		feedback (str): General feedback for question
	"""

    def __init__(self, docs, renderer=HTMLRenderer):
        """
		Create a question with parsed MD data
		Raises an error if any issue found
		"""
        self.title = ''
        self.ident = 'md2qti_question_' + uuid.uuid4().hex
        self.points = -1
        self.question = ''
        self.answers = []
        self.keys = []
        self.matchingKey = []
        self.matchingVal = []
        self.qtype = -1
        self.feedback = ''
        self.in_question = False
        self.in_answer = False

        with renderer() as renderer:
            for doc in docs:
                if doc.__class__.__name__ == 'CodeFence':
                    if not self.in_question:
                        raise Exception('\'\`\`\`\' code block should be inside \'@question\'')
                    pass
                if doc.__class__.__name__ == 'Setting' and doc.option == 'question':
                    self.in_question = True
                elif doc.__class__.__name__ == 'Setting' and doc.option == 'answer':
                    self.in_question = False
                    self.in_answer = True
                elif doc.__class__.__name__ == 'Setting' and doc.option == 'feedback':
                    self.feedback += renderer.render(Document(doc.content))
                elif self.in_question:
                    self.question += renderer.render(doc)
                elif self.in_answer:
                    self.setAnswer(doc)
                elif doc.__class__.__name__ == 'Setting':
                    self.setOption(doc)

    def setOption(self, doc):
        """
		Extract option from '@' setting
		"""
        if self.in_question:
            raise Exception('\'@ answer:\' is expected but not found.')
        elif self.in_answer:
            raise Exception('\'---\' is expected at the end of a question.')
        elif doc.option == 'title':
            self.title = doc.content
        elif doc.option == 'points':
            self.points = int(doc.content)
        elif doc.option == 'question':
            self.question = doc.content
        elif doc.option == 'type':
            self.qtype = Qtype.getQtype(doc.content)
            if self.qtype < 0:
                raise Exception(doc.content + ' is not a correct question type.')
        elif doc.option == 'feedback':
            self.feedback = doc.content

    def setAnswer(self, doc):
        """
		Unwrap parsed MD and populate an answer
		"""
        # Question type code
        # 'multiple choice': 1,
        # 'multiple answer': 2,
        # 'numerical': 3,
        # 'formula': 4,
        # 'essay': 5,
        # 'blank': 6,
        # 'multiple blank': 7,
        # 'matching': 8,
        # 'multiple dropdown': 9,
        # 'file': 10,
        # 'text': 11
        alphabet_string = string.ascii_uppercase
        alphabet_list = list(alphabet_string)

        if self.qtype == 1 or self.qtype == 2 or self.qtype == 6:  # multiple choice/answer, blank
            i = 0
            if doc.__class__.__name__ == 'List':
                for item in doc.children:
                    self.answers.append(MultipleChoice(item))
                for answer in self.answers:
                    answer.setId(alphabet_list[i])
                    i += 1
            else:
                raise Exception('Answer format is incorrect1.')
        elif self.qtype == 3:  # numerical
            if doc.__class__.__name__ == 'Quote':
                self.answers.append(Numerical(doc))
                self.answers[0].setId('A')
            else:
                raise Exception('Answer format is incorrect2.')
        elif self.qtype == 4:  # formula
            if not self.answers:
                self.answers.append(Formula())
            if doc.__class__.__name__ == 'List' and doc.children[0].leader == '-':
                for var in doc.children:
                    self.answers[0].setVar(var)
            elif doc.__class__.__name__ == 'List' and doc.children[0].leader == '*':
                self.answers[0].setFormula(doc.children[0])
            elif doc.__class__.__name__ == 'Quote':
                self.answers[0].setAnswer(doc.children[0])
            else:
                raise Exception('Answer format is incorrect3.')
        elif self.qtype == 7 or self.qtype == 8 or self.qtype == 9:  # matching, multiple blanks/dropdown
            if doc.__class__.__name__ == 'List' and doc.children[0].leader == '+':
                for key in doc.children:
                    for item in key.children[1].children:
                        self.answers.append(Matching(item, key.children[0]))
                i = 0
                for answer in self.answers:
                    if answer.key not in self.keys:
                        self.keys.append(answer.key)
                    answer.setId(alphabet_list[i])
                    self.matchingKey.append(str(i))
                    self.matchingVal.append(alphabet_list[i])
                    i += 1
            else:
                raise Exception('Answer format is incorrect for matching')
        elif self.qtype == 5 or self.qtype == 10 or self.qtype == 11:  # essay, file, text
            raise Exception('Answer is not required for essay, file, text question-type')

    def debug(self):
        """
		Print all members for debug purpose
		"""
        print('title:', self.title)
        print('ident:', self.ident)
        print('points:', self.points)
        print('qtype:', self.qtype)
        print('question:', self.question)
        for a in self.answers:
            a.debug()
        print('feedback:', self.feedback)


class ParsedGroup(Group):
    """
	Questions can be populated in a group and randomly picked
	* 'points per question' will overwrite the points of each question

	Attr:
		pick (int): The number of questions that will be picked
		ppq (int): Points Per Question
		ident (str): Question unique identifier
		qtype (str): Hard coded to 'group' type for generator purposes
		questions (List[Question]): List of questions
	"""

    def __init__(self):
        self.pick = -1
        self.ppq = -1
        self.questions = []
        self.ident = uuid.uuid4().hex
        self.qtype = 0

    def setPick(self, pick):
        if self.pick != -1:
            raise Exception('Pick is already defined')
        else:
            self.pick = int(pick)

    def setPpq(self, ppq):
        if self.ppq != -1:
            raise Exception('Points per question is already defined')
        else:
            self.ppq = int(ppq)

    def debug(self):
        print(f'ident:', self.ident)
        print(f'Group pick: {self.pick}')
        print(f'Group points per question: {self.ppq}')
        print(f'Group size of questions list: {len(self.questions)}')


class ParsedQuiz(Quiz):
    """
	Holds all information of the quiz

	Attr:
		title (str): Quiz title
		desc (str): Quiz description
		ident (str): Quiz unique identifier
		questions (List): List of Group and Question. They are populated
		into one list to follow the order of questions in MD file.
	"""

    def __init__(self, filename):
        self.title = ''
        self.description = ''
        self.ident = uuid.uuid4().hex
        self.assessmentIdent = uuid.uuid4().hex
        self.questions = []

        try:
            f = open(filename, "r")
        except OSError:
            print(f'Cannot open file: {filename}')
        with f:
            document = Document(f.read())

        in_group = False
        group = None
        docs = []

        for i, doc in enumerate(document.children):
            try:
                if doc.__class__.__name__ == 'CodeFence':
                    # pass
                    # Send doc.rawText to code script runner and put the result back into the list
                    # print(doc.language)
                    # print(doc.rawText)
                    save_stdout = sys.stdout
                    result = StringIO()
                    sys.stdout = result
                    exec(doc.rawText)
                    sys.stdout = save_stdout
                    result_string = result.getvalue()
                    newDocs = Document(result_string)
                    document.children[i + 1:i + 2] = newDocs.children
                elif doc.__class__.__name__ == 'Setting' and doc.option == 'quiz title':
                    self.setTitle(doc.content)
                elif doc.__class__.__name__ == 'Setting' and doc.option == 'quiz description':
                    self.setDescription(doc.content)
                elif doc.__class__.__name__ == 'Setting' and doc.option == 'group' and doc.content == 'start':
                    in_group = True
                    group = ParsedGroup()
                elif doc.__class__.__name__ == 'Setting' and doc.option == 'pick' and in_group:
                    group.setPick(doc.content)
                elif doc.__class__.__name__ == 'Setting' and doc.option == 'points per question' and in_group:
                    group.setPpq(doc.content)
                elif doc.__class__.__name__ == 'Setting' and doc.option == 'group' and doc.content == 'end':
                    in_group = False
                    self.questions.append(group)
                elif doc.__class__.__name__ == 'ThematicBreak' or i == len(document.children) - 1:
                    if not docs:
                        continue
                    if in_group:
                        group.questions.append(ParsedQuestion(docs))
                    else:
                        self.questions.append(ParsedQuestion(docs))
                    docs.clear()
                else:
                    docs.append(doc)
            except Exception as e:
                print('Error:', e)

    def setTitle(self, title):
        if self.title != '':
            raise Exception('Quiz title is already defined')
        else:
            self.title = title

    def setDescription(self, desc):
        if self.description != '':
            raise Exception('Quiz description is already defined')
        else:
            self.description = desc

    def debug(self):
        print(f'Quiz title: {self.title}')
        print(f'Quiz description: {self.description}')
        print(f'Quiz ident: {self.ident}')


def MetadataContent(quizData):
    # Metadata information
    data = ET.Element('quiz', {
        'xsi:schemaLocation': 'http://canvas.instructure.om/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd',
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xmlns': 'http//canvas.instructure.com/xsd/cccv1p0',
        'identifer': 'md2qti_assessment_' + quizData.ident})

    title = ET.SubElement(data, 'title')
    title.text = quizData.title
    description = ET.SubElement(data, 'description')
    description.text = quizData.description
    shuffle = ET.SubElement(data, 'shuffle_answers')
    shuffle.text = 'false'
    scoring = ET.SubElement(data, 'scoring_policy')
    scoring.text = 'keep_highest'
    hide = ET.SubElement(data, 'hide_results')
    quiztype = ET.SubElement(data, 'quiz_type')
    quiztype.text = 'assignment'
    pointspossible = ET.SubElement(data, 'points_possible')
    pointspossible.text = str(getTotalPoints(quizData))
    require1 = ET.SubElement(data, 'require_lockdown_browser')
    require1.text = 'false'
    require2 = ET.SubElement(data, 'require_lockdown_browser_for_results')
    require2.text = 'false'
    require3 = ET.SubElement(data, 'require_lockdown_browser_monitor')
    require3.text = 'false'
    lockdown = ET.SubElement(data, 'lockdown_browser_monitor_data')
    showcorrect = ET.SubElement(data, 'show_correct_answers')
    showcorrect.text = 'true'
    anonymoussubmission = ET.SubElement(data, 'anonymous_submissions')
    anonymoussubmission.text = 'false'
    couldbelocked = ET.SubElement(data, 'could_be_locked')
    couldbelocked.text = 'false'
    attempts = ET.SubElement(data, 'allowed_attempts')
    attempts.text = '1'
    onequestion = ET.SubElement(data, 'one_question_at_a_time')
    onequestion.text = 'false'
    cantgoback = ET.SubElement(data, 'cant_go_back')
    cantgoback.text = 'false'
    available = ET.SubElement(data, 'available')
    available.text = 'false'
    onetime = ET.SubElement(data, 'one_time_results')
    onetime.text = 'false'
    showcorrect = ET.SubElement(data, 'show_correct_answers_last_attempt')
    showcorrect.text = 'false'
    onlyvisible = ET.SubElement(data, 'only_visible_to_overrides')
    onlyvisible.text = 'false'
    module = ET.SubElement(data, 'module_locked')
    module.text = 'false'

    assignment = ET.SubElement(data, 'assignment', {'identifer': 'md2qti_assessment_' + quizData.ident})
    title = ET.SubElement(assignment, 'title')
    title.text = quizData.title
    dueat = ET.SubElement(assignment, 'due_at')
    lockat = ET.SubElement(assignment, 'lock_at')
    unlockat = ET.SubElement(assignment, 'unlock_at')
    module = ET.SubElement(assignment, 'module_locked')
    module.text = 'false'
    workflow = ET.SubElement(assignment, 'workflow_state')
    workflow.text = 'unpublished'
    assignmentoverride = ET.SubElement(assignment, 'assignment_override')
    assignmentoverride.text = ' '
    quizident = ET.SubElement(assignment, 'quiz_identifierref')
    quizident.text = 'md2qti_assessment_' + quizData.ident
    allowed = ET.SubElement(assignment, 'allowed_extensions')
    hasgroupcategory = ET.SubElement(assignment, 'has_group_category')
    hasgroupcategory.text = 'false'
    pointspossible = ET.SubElement(assignment, 'points_possible')
    pointspossible.text = str(getTotalPoints(quizData))
    gradingtype = ET.SubElement(assignment, 'grading_type')
    gradingtype.text = 'points'
    allday = ET.SubElement(assignment, 'all_day')
    allday.text = 'false'
    submissiontype = ET.SubElement(assignment, 'submission_types')
    submissiontype.text = 'online_quiz'
    position = ET.SubElement(assignment, 'position')
    position.text = '1'
    turnitin = ET.SubElement(assignment, 'turnitin_enabled')
    turnitin.text = 'false'
    vericite = ET.SubElement(assignment, 'vericite_enabled')
    vericite.text = 'false'
    peerreviewcount = ET.SubElement(assignment, 'peer_review_count')
    peerreviewcount.text = '0'
    peerreview = ET.SubElement(assignment, 'peer_review')
    peerreview.text = 'false'
    automaticpeer = ET.SubElement(assignment, 'automatic_peer_reviews')
    automaticpeer.text = 'false'
    anonymouspeer = ET.SubElement(assignment, 'anonymous_peer_reviews')
    anonymouspeer.text = 'false'
    gradegroup = ET.SubElement(assignment, 'grade_group_students_individually')
    gradegroup.text = 'false'
    freezeoncopy = ET.SubElement(assignment, 'freeze_on_copy')
    freezeoncopy.text = 'false'
    omitfinal = ET.SubElement(assignment, 'omit_from_final_grade')
    omitfinal.text = 'false'
    intragrouppeer = ET.SubElement(assignment, 'intra_group_peer_reviews')
    intragrouppeer.text = 'false'
    visibletooverride = ET.SubElement(assignment, 'only_visible_to_overrides')
    visibletooverride.text = 'false'
    posttosis = ET.SubElement(assignment, 'post_to_sis')
    posttosis.text = 'false'
    moderatedgrade = ET.SubElement(assignment, 'moderated_grading')
    moderatedgrade.text = 'false'
    gradercount = ET.SubElement(assignment, 'grader_count')
    gradercount.text = '0'
    gradercomment = ET.SubElement(assignment, 'grader_comments_visible_to_graders')
    gradercomment.text = 'true'
    anongrade = ET.SubElement(assignment, 'anonymous_grading')
    anongrade.text = 'false'
    gradeanongrade = ET.SubElement(assignment, 'graders_anonymous_to_grades')
    gradeanongrade.text = 'false'
    gradernames = ET.SubElement(assignment, 'grader_names_visible_final_grader')
    gradernames.text = 'true'
    anoninstructor = ET.SubElement(assignment, 'anonymous_instructor_annotations')
    anoninstructor.text = 'false'
    postpolicy = ET.SubElement(assignment, 'post_policy')
    postmanually = ET.SubElement(postpolicy, 'post_manually')
    postmanually.text = 'false'

    assignmentgroup = ET.SubElement(data, 'assignment_group_identifierref' + quizData.ident)
    assignmentgroup.text = 'md2qti_assignment-group_' + quizData.ident
    assignmentoverride = ET.SubElement(data, 'assignment_override')
    assignmentoverride.text = ' '

    return data


def getTotalPoints(quiz):
    total = 0
    for item in quiz.questions:
        if item.qtype == 0:
            total += item.pick * item.ppq
        else:
            total += item.points
    return total


def IMSContent(quizData):
    today = date.today()
    todayFormatted = today.strftime("%Y-%m-%d")

    # Manifest information
    data = ET.Element('manifest', {
        'xsi:schemaLocation': 'http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1 http://www.imsglobal.org/xsd/imscp_v1p1.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lomresource_v1p0.xsd http://www.imsglobal.org/xsd/imsmd_v1p2 http://www.imsglobal.org/xsd/imsmd_v1p2p2/xsd',
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xmlns:imsmd': 'http://www.imsglobal.org/xsd/imsmd_v1p2',
        'xmlns:lom': 'http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource',
        'xmlns': 'http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1',
        'identifer': 'md2qti_manifest_' + quizData.ident})
    # data = ET.Element('testtest')
    metadata = ET.SubElement(data, 'metadata')
    schema = ET.SubElement(metadata, 'schema')
    schemaversion = ET.SubElement(metadata, 'schemaversion')
    schema.text = 'IMS Content'
    schemaversion.text = '1.1.3'
    imsmdlom = ET.SubElement(metadata, 'imsmd:lom')
    imsmdgeneral = ET.SubElement(imsmdlom, 'imsmd:general')
    imsmdtitle = ET.SubElement(imsmdgeneral, 'imsmd:title')
    imsmdstring = ET.SubElement(imsmdtitle, 'imsmd:string')
    imsmdstring.text = 'QTI assessment generated by md2qti'
    imsmdlifecycle = ET.SubElement(imsmdlom, 'imsmd:lifeCycle')
    imsmdcontribute = ET.SubElement(imsmdlifecycle, 'imsmd:contribute')
    imsmddate = ET.SubElement(imsmdcontribute, 'imsmd:date')
    imsmddatetime = ET.SubElement(imsmddate, 'imsmd:dateTime')
    imsmddatetime.text = todayFormatted
    imsmdrights = ET.SubElement(imsmdlom, 'imsmd:rights')
    imsmdcopyright = ET.SubElement(imsmdrights, 'imsmd:copyrightAndOtherRestrictions')
    imsmdvalue = ET.SubElement(imsmdcopyright, 'imsmd:value')
    imsmdvalue.text = 'yes'
    imsmddescription = ET.SubElement(imsmdrights, 'imsmd:description')
    imsmdstring = ET.SubElement(imsmddescription, 'imsmd:string')
    imsmdstring.text = 'Private (Copyrighted) - http://en.wikipedia.org/wiki/Copyright'

    organizations = ET.SubElement(data, 'organizations')

    resources = ET.SubElement(data, 'resources')
    resource = ET.SubElement(resources, 'resource',
                             {'identifier': 'md2qti_assessment_' + quizData.ident, 'type': 'imsqti_xmlv1p2'})
    file = ET.SubElement(resource, 'file', {
        'href': 'md2qti_assessment_' + quizData.ident + '/' + 'md2qti_assessment_' + quizData.ident + '.xml'})
    dependency = ET.SubElement(resource, 'dependency',
                               {'identifierref': 'md2qti_dependency_' + quizData.assessmentIdent})
    resource = ET.SubElement(resources, 'resource', {'identifier': 'md2qti_dependency_' + quizData.assessmentIdent,
                                                     'type': 'associatedcontent/imscc_xmlv1p1/learning-application-resource',
                                                     'href': quizData.ident + '/assessment_meta.xml'})
    file = ET.SubElement(resource, 'file', {'href': 'md2qti_assessment_' + quizData.ident + '/assessment_meta.xml'})

    return data


def Generator(quizData):
    # Document information
    data = ET.Element('questestinterop', {'xmlns': 'http://www.imsglobal.org/xsd/ims_qtiasiv1p2',
                                          'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                                          'xsi:schemaLocation': 'http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd'})
    assessment = ET.SubElement(data, 'assessment', {
        'ident': quizData.ident,
        'title': quizData.title})
    # QTI metadata
    qtimetadata = ET.SubElement(assessment, 'qtimetadata')
    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
    fieldlabel.text = 'cc_maxattempts'
    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
    fieldentry.text = '1'

    mainSection = ET.SubElement(assessment, 'section', {'ident': 'root_section'})

    # For loop through MDQuiz.questions
    for item in quizData.questions:
        # If group of questions
        if item.qtype == 0:
            groupSection = ET.SubElement(mainSection, 'section', {'title': 'Group', 'ident': item.ident})
            selection_ordering = ET.SubElement(groupSection, 'selection_ordering')
            selection = ET.SubElement(selection_ordering, 'selection')
            selection_number = ET.SubElement(selection, 'selection_number')
            selection_number.text = str(item.pick)
            selection_extension = ET.SubElement(selection, 'selection_extension')
            points_per_item = ET.SubElement(selection_extension, 'points_per_items')
            points_per_item.text = str(item.ppq)

            selectedQuestions = random.sample(item.questions, item.pick)
            for question in selectedQuestions:
                question.points = item.ppq
                getQuestionXML(question, groupSection)
        else:
            getQuestionXML(item, mainSection)
    return data


def getQuestionXML(question, parentElement):
    # multiple choice: 1,
    if question.qtype == 1:
        multiple_choice(question, parentElement)
    # multiple answer: 2,
    elif question.qtype == 2:
        multiple_answer(question, parentElement)
    # numerical: 3,
    elif question.qtype == 3:
        numerical(question, parentElement)
    # formula: 4,
    elif question.qtype == 4:
        formula(question, parentElement)
    # essay: 5,
    elif question.qtype == 5:
        essay(question, parentElement)
    # blank: 6,
    elif question.qtype == 6:
        fill_in_the_blank(question, parentElement)
    # multiple blank: 7,
    elif question.qtype == 7:
        fill_in_multiple_blank(question, parentElement)
    # 'matching': 8,
    elif question.qtype == 8:
        matching(question, parentElement)
    # multiple dropdown: 9,
    elif question.qtype == 9:
        multiple_dropdown(question, parentElement)
    # file: 10,
    elif question.qtype == 10:
        file_upload(question, parentElement)
    # text: 11
    elif question.qtype == 11:
        text_only(question, parentElement)
    else:
        raise Exception('Invalid question format!')


def setItemMetaData(question, parentElement):
    answerIds = ''
    questionType = ''
    if question.qtype == 1:
        questionType = 'multiple_choice_question'
    elif question.qtype == 2:
        questionType = 'multiple_answers_question'
    elif question.qtype == 3:
        questionType = 'numerical_question'
    elif question.qtype == 4:
        questionType = 'calculated_question'
    elif question.qtype == 5:
        questionType = 'essay_question'
    elif question.qtype == 6:
        questionType = 'short_answer_question'
    elif question.qtype == 7:
        questionType = 'fill_in_multiple_blanks_question'
    elif question.qtype == 8:
        questionType = 'matching_question'
    elif question.qtype == 9:
        questionType = 'multiple_dropdowns_question'
    elif question.qtype == 10:
        questionType = 'file_upload_question'
    elif question.qtype == 11:
        questionType = 'text_only_question'
    for choices in question.answers:
        if answerIds == '':
            answerIds = choices.ident
        else:
            answerIds = answerIds + ',' + choices.ident

    itemmetadata = ET.SubElement(parentElement, 'itemmetadata')
    qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
    fieldlabel.text = 'question_type'
    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
    fieldentry.text = questionType
    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
    fieldlabel.text = 'points_possible'
    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
    fieldentry.text = str(question.points)
    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
    fieldlabel.text = 'original_answer_ids'
    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
    fieldentry.text = answerIds
    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
    fieldlabel.text = 'assessment_question_identifierref'
    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
    fieldentry.text = question.ident


def setFeedback(question, parentElement):
    if question.feedback != '':
        itemfeedback = ET.SubElement(parentElement, 'itemfeedback', {'ident': 'general_fb'})
        flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
        material = ET.SubElement(flow_mat, 'material')
        mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
        mattext.text = question.feedback
    for answer in question.answers:
        if answer.feedback != '':
            itemfeedback = ET.SubElement(parentElement, 'itemfeedback', {'ident': answer.ident + '_fb'})
            flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
            material = ET.SubElement(flow_mat, 'material')
            mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
            mattext.text = answer.feedback


def setGeneralFeedback(parentElement):
    respcondition = ET.SubElement(parentElement, 'respcondition', {'continue': 'Yes'})
    conditionvar = ET.SubElement(respcondition, "conditionvar")
    other = ET.SubElement(conditionvar, "other")
    displayfeedback = ET.SubElement(respcondition, 'displayfeedback', {'linkrefid': 'general_fb',
                                                                       'feedbacktype': 'Response'})


def multiple_choice(question, parentElement):
    correctChoice = ''
    item = ET.SubElement(parentElement, 'item', {'ident': question.ident, 'title': question.title})
    # Item metadata
    setItemMetaData(question, item)

    # Presentation
    presentation = ET.SubElement(item, 'presentation')
    material = ET.SubElement(presentation, 'material')
    mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
    mattext.text = question.question

    response_lid = ET.SubElement(presentation, 'response_lid', {'ident': 'response1', 'rcardinality': 'Single'})
    render_choice = ET.SubElement(response_lid, 'render_choice')
    for answer in question.answers:
        response_label = ET.SubElement(render_choice, 'response_label', {'ident': answer.ident})
        material = ET.SubElement(response_label, 'material')
        mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
        mattext.text = answer.val

    # Response processing
    resprocessing = ET.SubElement(item, 'resprocessing')
    outcomes = ET.SubElement(resprocessing, 'outcomes')
    decvar = ET.SubElement(outcomes, 'decvar', {'maxvalue': '100',
                                                'minvalue': '0',
                                                'varname': 'SCORE',
                                                'vartype': 'Decimal'})
    if question.feedback != '':
        setGeneralFeedback(resprocessing)

    for answer in question.answers:
        if answer.is_correct:
            correctChoice = answer.ident
        if answer.feedback != '':
            respcondition = ET.SubElement(resprocessing, 'respcondition', {'continue': 'Yes'})
            conditionvar = ET.SubElement(respcondition, "conditionvar")
            varequal = ET.SubElement(conditionvar, "varequal", {'respident': 'response1'})
            varequal.text = answer.ident
            displayfeedback = ET.SubElement(respcondition, 'displayfeedback', {'linkrefid': answer.ident + '_fb',
                                                                               'feedbacktype': 'Response'})
    respcondition = ET.SubElement(resprocessing, 'respcondition', {'continue': 'No'})
    conditionvar = ET.SubElement(respcondition, 'conditionvar')
    varequal = ET.SubElement(conditionvar, 'varequal', {'respident': 'response1'})
    varequal.text = correctChoice
    setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Set', 'varname': 'SCORE'})
    setvar.text = '100'

    # feedback
    setFeedback(question, item)


def multiple_answer(question, parentElement):
    item = ET.SubElement(parentElement, 'item', {'ident': question.ident, 'title': question.title})
    # Item metadata
    setItemMetaData(question, item)

    # Presentation
    presentation = ET.SubElement(item, 'presentation')
    material = ET.SubElement(presentation, 'material')
    mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
    mattext.text = question.question

    response_lid = ET.SubElement(presentation, 'response_lid', {'ident': 'response1', 'rcardinality': 'Multiple'})
    render_choice = ET.SubElement(response_lid, 'render_choice')
    for answer in question.answers:
        response_label = ET.SubElement(render_choice, 'response_label', {'ident': answer.ident})
        material = ET.SubElement(response_label, 'material')
        mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/plain'})
        mattext.text = answer.val

    # Response processing
    resprocessing = ET.SubElement(item, 'resprocessing')
    outcomes = ET.SubElement(resprocessing, 'outcomes')
    decvar = ET.SubElement(outcomes, 'decvar', {'maxvalue': '100',
                                                'minvalue': '0',
                                                'varname': 'SCORE',
                                                'vartype': 'Decimal'})
    if question.feedback != '':
        setGeneralFeedback(resprocessing)
    for answer in question.answers:
        if answer.feedback != '':
            respcondition = ET.SubElement(resprocessing, 'respcondition', {'continue': 'Yes'})
            conditionvar = ET.SubElement(respcondition, "conditionvar")
            varequal = ET.SubElement(conditionvar, "varequal", {'respident': 'response1'})
            varequal.text = answer.ident
            displayfeedback = ET.SubElement(respcondition, 'displayfeedback', {'linkrefid': answer.ident + '_fb',
                                                                               'feedbacktype': 'Response'})
    respcondition = ET.SubElement(resprocessing, 'respcondition', {'continue': 'No'})
    conditionvar = ET.SubElement(respcondition, 'conditionvar')
    andtag = ET.SubElement(conditionvar, 'and')
    for answer in question.answers:
        if answer.is_correct:
            varequal = ET.SubElement(andtag, 'varequal', {'respident': 'response1'})
            varequal.text = answer.ident
        else:
            nottag = ET.SubElement(andtag, 'not')
            varequal = ET.SubElement(nottag, 'varequal', {'respident': 'response1'})
            varequal.text = answer.ident
    setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Set', 'varname': 'SCORE'})
    setvar.text = '100'

    # feedback
    setFeedback(question, item)


def numerical(question, parentElement):
    item = ET.SubElement(parentElement, 'item', {'ident': question.ident, 'title': question.title})
    # Item metadata
    setItemMetaData(question, item)

    # Presentation
    presentation = ET.SubElement(item, 'presentation')
    material = ET.SubElement(presentation, 'material')
    mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
    mattext.text = question.question

    response_str = ET.SubElement(presentation, 'response_str', {'ident': 'response1', 'rcardinality': 'Single'})
    render_fib = ET.SubElement(response_str, 'render_fib', {'fibtype': 'Decimal'})
    response_label = ET.SubElement(render_fib, 'response_label', {'ident': 'answer1'})

    # Response processing
    answer = question.answers[0]
    exactNumber = answer.val
    margin = answer.margin
    lowerBoundNumber = str(exactNumber - margin)
    upperBoundNumber = str(exactNumber + margin)
    resprocessing = ET.SubElement(item, 'resprocessing')
    outcomes = ET.SubElement(resprocessing, 'outcomes')
    decvar = ET.SubElement(outcomes, 'decvar', {'maxvalue': '100',
                                                'minvalue': '0',
                                                'varname': 'SCORE',
                                                'vartype': 'Decimal'})
    if question.feedback != '':
        setGeneralFeedback(resprocessing)
    respcondition = ET.SubElement(resprocessing, 'respcondition', {'continue': 'No'})
    conditionvar = ET.SubElement(respcondition, 'conditionvar')
    ortag = ET.SubElement(conditionvar, 'or')
    varequal = ET.SubElement(ortag, 'varequal', {'respident': 'response1'})
    varequal.text = str(exactNumber)
    andtag = ET.SubElement(ortag, 'and')
    vargte = ET.SubElement(andtag, 'vargte', {'respident': 'response1'})
    vargte.text = lowerBoundNumber
    varlte = ET.SubElement(andtag, 'varlte', {'respident': 'response1'})
    varlte.text = upperBoundNumber
    setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Set', 'varname': 'SCORE'})
    setvar.text = '100'
    if answer.feedback != '':
        displayfeedback = ET.SubElement(respcondition, 'displayfeedback', {'linkrefid': answer.ident + '_fb',
                                                                           'feedbacktype': 'Response'})
    # feedback
    setFeedback(question, item)


def formula(question, parentElement):
    item = ET.SubElement(parentElement, 'item', {'ident': question.ident, 'title': question.title})
    # Item metadata
    choice = question.answers[0]
    answerIds = ''
    for i in range(len(choice.generatedValues)):
        if answerIds == '':
            answerIds = choice.generatedValues[i][-1][0]
        else:
            answerIds = answerIds + ',' + choice.generatedValues[i][-1][0]
    itemmetadata = ET.SubElement(item, 'itemmetadata')
    qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
    fieldlabel.text = 'question_type'
    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
    fieldentry.text = 'calculated_question'
    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
    fieldlabel.text = 'points_possible'
    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
    fieldentry.text = str(question.points)
    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
    fieldlabel.text = 'original_answer_ids'
    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
    fieldentry.text = answerIds
    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
    fieldlabel.text = 'assessment_question_identifierref'
    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
    fieldentry.text = question.ident

    # Presentation
    presentation = ET.SubElement(item, 'presentation')
    material = ET.SubElement(presentation, 'material')
    mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
    mattext.text = question.question

    response_str = ET.SubElement(presentation, 'response_str', {'ident': 'response1', 'rcardinality': 'Single'})
    render_fib = ET.SubElement(response_str, 'render_fib', {'fibtype': 'Decimal'})
    response_label = ET.SubElement(render_fib, 'response_label', {'ident': 'answer1'})

    # Response processing
    resprocessing = ET.SubElement(item, 'resprocessing')
    outcomes = ET.SubElement(resprocessing, 'outcomes')
    decvar = ET.SubElement(outcomes, 'decvar', {'maxvalue': '100',
                                                'minvalue': '0',
                                                'varname': 'SCORE',
                                                'vartype': 'Decimal'})
    if question.feedback != '':
        setGeneralFeedback(resprocessing)
    respcondition = ET.SubElement(resprocessing, 'respcondition', {'title': 'correct'})
    conditionvar = ET.SubElement(respcondition, 'conditionvar')
    other = ET.SubElement(conditionvar, 'other')
    setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Set', 'varname': 'SCORE'})
    setvar.text = '100'
    respcondition = ET.SubElement(resprocessing, 'respcondition', {'title': 'incorrect'})
    conditionvar = ET.SubElement(respcondition, 'conditionvar')
    nottag = ET.SubElement(conditionvar, 'not')
    other = ET.SubElement(nottag, 'other')
    setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Set', 'varname': 'SCORE'})
    setvar.text = '0'

    # Extension
    itemproc_extension = ET.SubElement(item, 'itemproc_extension')
    calculated = ET.SubElement(itemproc_extension, 'calculated')
    answer_tolerance = ET.SubElement(calculated, 'answer_tolerance')
    answer_tolerance.text = str(choice.margin)
    formulas = ET.SubElement(calculated, 'formulas', {'decimal_places': choice.vars[0][3]})
    formula = ET.SubElement(formulas, 'formula')
    formula.text = choice.formula
    vars = ET.SubElement(calculated, 'vars')
    for variable in choice.vars:
        var = ET.SubElement(vars, 'var', {'scale': variable[3], 'name': variable[0]})
        min = ET.SubElement(var, 'min')
        min.text = variable[1]
        max = ET.SubElement(var, 'max')
        max.text = variable[2]
    var_sets = ET.SubElement(calculated, 'var_sets')
    for values in choice.generatedValues:
        var_set = ET.SubElement(var_sets, 'var_set', {'ident': values[-1][0]})
        for j in range(len(values) - 1):
            var = ET.SubElement(var_set, 'var', {'name': values[j][0]})
            var.text = str(values[j][1])
        answer = ET.SubElement(var_set, 'answer')
        answer.text = str(values[-1][1])

    # feedback
    setFeedback(question, item)


def essay(question, parentElement):
    item = ET.SubElement(parentElement, 'item', {'ident': question.ident, 'title': question.title})
    # Item metadata
    setItemMetaData(question, item)

    # Presentation
    presentation = ET.SubElement(item, 'presentation')
    material = ET.SubElement(presentation, 'material')
    mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
    mattext.text = question.question

    response_str = ET.SubElement(presentation, 'response_str', {'ident': 'response1', 'rcardinality': 'Single'})
    render_fib = ET.SubElement(response_str, 'render_fib')
    response_label = ET.SubElement(render_fib, 'response_label', {'ident': 'answer1', 'rshuffle': 'No'})

    # Response processing
    resprocessing = ET.SubElement(item, 'resprocessing')
    outcomes = ET.SubElement(resprocessing, 'outcomes')
    decvar = ET.SubElement(outcomes, 'decvar', {'maxvalue': '100',
                                                'minvalue': '0',
                                                'varname': 'SCORE',
                                                'vartype': 'Decimal'})
    if question.feedback != '':
        setGeneralFeedback(resprocessing)
    respcondition = ET.SubElement(resprocessing, 'respcondition', {'continue': 'No'})
    conditionvar = ET.SubElement(respcondition, 'conditionvar')
    other = ET.SubElement(conditionvar, 'other')
    # feedback
    setFeedback(question, item)


def fill_in_the_blank(question, parentElement):
    item = ET.SubElement(parentElement, 'item', {'ident': question.ident, 'title': question.title})
    # Item metadata
    setItemMetaData(question, item)

    # Presentation
    presentation = ET.SubElement(item, 'presentation')
    material = ET.SubElement(presentation, 'material')
    mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
    mattext.text = question.question

    response_str = ET.SubElement(presentation, 'response_str', {'ident': 'response1', 'rcardinality': 'Single'})
    render_fib = ET.SubElement(response_str, 'render_fib')
    response_label = ET.SubElement(render_fib, 'response_label', {'ident': 'answer1', 'rshuffle': 'No'})

    # Response processing
    resprocessing = ET.SubElement(item, 'resprocessing')
    outcomes = ET.SubElement(resprocessing, 'outcomes')
    decvar = ET.SubElement(outcomes, 'decvar', {'maxvalue': '100',
                                                'minvalue': '0',
                                                'varname': 'SCORE',
                                                'vartype': 'Decimal'})
    if question.feedback != '':
        setGeneralFeedback(resprocessing)

    for answer in question.answers:
        if answer.feedback != '':
            respcondition = ET.SubElement(resprocessing, 'respcondition', {'continue': 'Yes'})
            conditionvar = ET.SubElement(respcondition, "conditionvar")
            varequal = ET.SubElement(conditionvar, "varequal", {'respident': 'response1'})
            varequal.text = answer.val
            displayfeedback = ET.SubElement(respcondition, 'displayfeedback', {'linkrefid': answer.ident + '_fb',
                                                                               'feedbacktype': 'Response'})
    respcondition = ET.SubElement(resprocessing, 'respcondition', {'continue': 'No'})
    conditionvar = ET.SubElement(respcondition, 'conditionvar')
    for answer in question.answers:
        varequal = ET.SubElement(conditionvar, 'varequal', {'respident': 'response1'})
        varequal.text = answer.val
    setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Set', 'varname': 'SCORE'})
    setvar.text = '100'

    # feedback
    setFeedback(question, item)


def fill_in_multiple_blank(question, parentElement):
    dividedScore = str(float(100 / len(question.keys)))
    item = ET.SubElement(parentElement, 'item', {'ident': question.ident, 'title': question.title})
    # Item metadata
    setItemMetaData(question, item)

    # Presentation
    presentation = ET.SubElement(item, 'presentation')
    material = ET.SubElement(presentation, 'material')
    mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
    mattext.text = question.question

    for key in question.keys:
        response_lid = ET.SubElement(presentation, 'response_lid', {'ident': 'response_' + key})
        material = ET.SubElement(response_lid, 'material')
        mattext = ET.SubElement(material, 'mattext')
        mattext.text = key
        render_choice = ET.SubElement(response_lid, 'render_choice')
        for answer in question.answers:
            if answer.key == key:
                response_label = ET.SubElement(render_choice, 'response_label', {'ident': answer.ident})
                material = ET.SubElement(response_label, 'material')
                mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/plain'})
                mattext.text = answer.val

    # Response processing
    resprocessing = ET.SubElement(item, 'resprocessing')
    outcomes = ET.SubElement(resprocessing, 'outcomes')
    decvar = ET.SubElement(outcomes, 'decvar', {'maxvalue': '100',
                                                'minvalue': '0',
                                                'varname': 'SCORE',
                                                'vartype': 'Decimal'})
    if question.feedback != '':
        setGeneralFeedback(resprocessing)
    for answer in question.answers:
        if answer.feedback != '':
            respcondition = ET.SubElement(resprocessing, 'respcondition', {'continue': 'Yes'})
            conditionvar = ET.SubElement(respcondition, 'conditionvar')
            varequal = ET.SubElement(conditionvar, "varequal", {'respident': 'response_' + answer.key})
            varequal.text = answer.ident
            displayfeedback = ET.SubElement(respcondition, 'displayfeedback', {'linkrefid': answer.ident + '_fb',
                                                                               'feedbacktype': 'Response'})
    for key in question.keys:
        respcondition = ET.SubElement(resprocessing, 'respcondition')
        conditionvar = ET.SubElement(respcondition, 'conditionvar')
        for answer in question.answers:
            if answer.key == key:
                varequal = ET.SubElement(conditionvar, "varequal", {'respident': 'response_' + key})
                varequal.text = answer.ident
        setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Add', 'varname': 'SCORE'})
        setvar.text = dividedScore

    # feedback
    setFeedback(question, item)


def matching(question, parentElement):
    numberOfValidKeys = 0
    for key in question.keys:
        if key != 'DISTRACTOR':
            numberOfValidKeys += 1
    dividedScore = str(float(100 / numberOfValidKeys))
    item = ET.SubElement(parentElement, 'item', {'ident': question.ident, 'title': question.title})

    # Item metadata
    answerIds = ''
    for i in range(0, numberOfValidKeys):
        if answerIds == '':
            answerIds = question.matchingKey[i]
        else:
            answerIds = answerIds + ',' + question.matchingKey[i]
    itemmetadata = ET.SubElement(item, 'itemmetadata')
    qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
    fieldlabel.text = 'question_type'
    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
    fieldentry.text = 'matching_question'
    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
    fieldlabel.text = 'points_possible'
    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
    fieldentry.text = str(question.points)
    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
    fieldlabel.text = 'original_answer_ids'
    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
    fieldentry.text = answerIds
    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
    fieldlabel.text = 'assessment_question_identifierref'
    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
    fieldentry.text = question.ident

    # Presentation
    presentation = ET.SubElement(item, 'presentation')
    material = ET.SubElement(presentation, 'material')
    mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
    mattext.text = question.question

    for keyIndex in range(0, numberOfValidKeys):
        response_lid = ET.SubElement(presentation, 'response_lid', {'ident': 'response_' + str(keyIndex)})
        material = ET.SubElement(response_lid, 'material')
        mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/plain'})
        mattext.text = question.answers[keyIndex].key
        render_choice = ET.SubElement(response_lid, 'render_choice')
        for valIndex in range(0, len(question.matchingVal)):
            response_label = ET.SubElement(render_choice, 'response_label', {'ident': question.matchingVal[valIndex]})
            material = ET.SubElement(response_label, 'material')
            mattext = ET.SubElement(material, 'mattext')
            mattext.text = question.answers[valIndex].val

    # Response processing
    resprocessing = ET.SubElement(item, 'resprocessing')
    outcomes = ET.SubElement(resprocessing, 'outcomes')
    decvar = ET.SubElement(outcomes, 'decvar', {'maxvalue': '100',
                                                'minvalue': '0',
                                                'varname': 'SCORE',
                                                'vartype': 'Decimal'})
    if question.feedback != '':
        setGeneralFeedback(resprocessing)
    for keyIndex in range(0, numberOfValidKeys):
        respcondition = ET.SubElement(resprocessing, 'respcondition')
        conditionvar = ET.SubElement(respcondition, 'conditionvar')
        varequal = ET.SubElement(conditionvar, "varequal", {'respident': 'response_' + str(keyIndex)})
        varequal.text = question.matchingVal[keyIndex]
        setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Add', 'varname': 'SCORE'})
        setvar.text = dividedScore
        if question.answers[keyIndex].feedback != '':
            respcondition = ET.SubElement(resprocessing, 'respcondition')
            conditionvar = ET.SubElement(respcondition, 'conditionvar')
            nottag = ET.SubElement(conditionvar, 'not')
            varequal = ET.SubElement(nottag, "varequal", {'respident': 'response_' + keyIndex})
            varequal.text = question.matchingVal[keyIndex]
            displayfeedback = ET.SubElement(respcondition, 'displayfeedback', {'linkrefid': str(keyIndex) + '_fb',
                                                                               'feedbacktype': 'Response'})

    # feedback
    if question.feedback != '':
        itemfeedback = ET.SubElement(item, 'itemfeedback', {'ident': 'general_fb'})
        flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
        material = ET.SubElement(flow_mat, 'material')
        mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
        mattext.text = question.feedback
    for keyIndex in range(0, numberOfValidKeys):
        if question.answers[keyIndex].feedback != '':
            itemfeedback = ET.SubElement(parentElement, 'itemfeedback', {'ident': str(keyIndex) + '_fb'})
            flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
            material = ET.SubElement(flow_mat, 'material')
            mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
            mattext.text = question.answers[keyIndex].feedback


def multiple_dropdown(question, parentElement):
    dividedScore = str(float(100 / len(question.keys)))
    item = ET.SubElement(parentElement, 'item', {'ident': question.ident, 'title': question.title})
    # Item metadata
    setItemMetaData(question, item)

    # Presentation
    presentation = ET.SubElement(item, 'presentation')
    material = ET.SubElement(presentation, 'material')
    mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
    mattext.text = question.question

    for key in question.keys:
        response_lid = ET.SubElement(presentation, 'response_lid', {'ident': 'response_' + key})
        material = ET.SubElement(response_lid, 'material')
        mattext = ET.SubElement(material, 'mattext')
        mattext.text = key
        render_choice = ET.SubElement(response_lid, 'render_choice')
        for answer in question.answers:
            if answer.key == key:
                response_label = ET.SubElement(render_choice, 'response_label', {'ident': answer.ident})
                material = ET.SubElement(response_label, 'material')
                mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/plain'})
                mattext.text = answer.val

    # Response processing
    resprocessing = ET.SubElement(item, 'resprocessing')
    outcomes = ET.SubElement(resprocessing, 'outcomes')
    decvar = ET.SubElement(outcomes, 'decvar', {'maxvalue': '100',
                                                'minvalue': '0',
                                                'varname': 'SCORE',
                                                'vartype': 'Decimal'})
    if question.feedback != '':
        setGeneralFeedback(resprocessing)
    for answer in question.answers:
        if answer.feedback != '':
            respcondition = ET.SubElement(resprocessing, 'respcondition', {'continue': 'Yes'})
            conditionvar = ET.SubElement(respcondition, 'conditionvar')
            varequal = ET.SubElement(conditionvar, "varequal", {'respident': 'response_' + answer.key})
            varequal.text = answer.ident
            displayfeedback = ET.SubElement(respcondition, 'displayfeedback', {'linkrefid': answer.ident + '_fb',
                                                                               'feedbacktype': 'Response'})
    for key in question.keys:
        respcondition = ET.SubElement(resprocessing, 'respcondition')
        conditionvar = ET.SubElement(respcondition, 'conditionvar')
        for answer in question.answers:
            if (answer.key == key) & (answer.is_correct):
                varequal = ET.SubElement(conditionvar, "varequal", {'respident': 'response_' + key})
                varequal.text = answer.ident
        setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Add', 'varname': 'SCORE'})
        setvar.text = dividedScore

    # feedback
    setFeedback(question, item)


def file_upload(question, parentElement):
    item = ET.SubElement(parentElement, 'item', {'ident': question.ident, 'title': question.title})
    # Item metadata
    setItemMetaData(question, item)

    # Presentation
    presentation = ET.SubElement(item, 'presentation')
    material = ET.SubElement(presentation, 'material')
    mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
    mattext.text = question.question

    # Response processing
    resprocessing = ET.SubElement(item, 'resprocessing')
    outcomes = ET.SubElement(resprocessing, 'outcomes')
    decvar = ET.SubElement(outcomes, 'decvar', {'maxvalue': '100',
                                                'minvalue': '0',
                                                'varname': 'SCORE',
                                                'vartype': 'Decimal'})
    if question.feedback != '':
        setGeneralFeedback(resprocessing)

    # feedback
    setFeedback(question, item)


def text_only(question, parentElement):
    item = ET.SubElement(parentElement, 'item', {'ident': question.ident, 'title': question.title})
    # Item metadata
    setItemMetaData(question, item)

    # Presentation
    presentation = ET.SubElement(item, 'presentation')
    material = ET.SubElement(presentation, 'material')
    mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
    mattext.text = question.question


if __name__ == '__main__':
    if len(sys.argv) < 2:
        filename = input("Enter file name: ")
    else:
        filename = sys.argv[1]

    # Parse the file into data
    quizData = ParsedQuiz(filename)

    # Generate ims manifest from data
    imsXML = IMSContent(quizData)
    imsContent = ET.tostring(imsXML)
    imsFile = open('imsmanifest.xml', 'wb')
    imsFile.write(imsContent)
    imsFile.close()

    # Create assessment folder
    contentPath = 'm2qti_assessment_' + quizData.ident
    try:
        os.mkdir(contentPath)
    except OSError:
        pass

    # Generate assessment metadata from data
    metadataFile = 'assessment_meta.xml'
    assessmentXML = MetadataContent(quizData)
    assessmentMetadata = ET.tostring(assessmentXML)
    metaFile = open(os.path.join(contentPath, metadataFile), 'wb')
    metaFile.write(assessmentMetadata)
    metaFile.close()

    # Generate quiz qti from data
    quizFile = 'md2qti_assessment_' + quizData.ident + '.xml'
    quizXML = Generator(quizData)
    quizContent = ET.tostring(quizXML)
    quizFile = open(os.path.join(contentPath, quizFile), 'wb')
    quizFile.write(quizContent)
    quizFile.close()

    # Zip the files
    with ZipFile('ExportedQTI.zip', 'w') as zipObj:
        zipObj.write('imsmanifest.xml')
        for dirname, subdirs, files in os.walk(contentPath):
            zipObj.write(dirname)
            for filename in files:
                zipObj.write(os.path.join(dirname, filename))

    # Delete the files
    os.remove('imsmanifest.xml')
    shutil.rmtree(contentPath)

# mdquiz.debug()
# for q in mdquiz.questions:
# 	if q.__class__.__name__ == 'MDGroup':
# 		print('--group-start--')
# 		print('points per question:', q.ppq)
# 		print('pick:', q.pick)
# 		for q2 in q.questions:
# 			q2.debug()
# 		print('--group-end--')
# 	else:
# 		q.debug()
# 		print('')
