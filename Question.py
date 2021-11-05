import string
import random

import sympy as sy
from typing import List
import mistletoe
from mistletoe import Document
from mistletoe.html_renderer import HTMLRenderer


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
