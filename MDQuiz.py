import sys
import mistletoe
from mistletoe import Document
from mistletoe.html_renderer import HTMLRenderer
from Question import *
from Quiz import *


class MDQuestion(Question):
	"""
	Information of each question

	Attr:
		title (str): Question title
		points (int): Question points
		question (str): Question instruction. escaped-html format
		answer (List[any]): Question answers. Format follows the question type
		qtype (str): Question type
		feedback (str): General feedback for question
	"""
	def __init__(self, docs, renderer = HTMLRenderer):
		"""
		Create a question with parsed MD data
		Raises an error if any issue found
		"""
		self.title = ''
		self.points = -1
		self.question = ''
		self.answers = []
		self.qtype = -1
		self.feedback = ''
		self.in_question = False
		self.in_answer = False

		with renderer() as renderer:
			for doc in docs:
				if doc.__class__.__name__ == 'CodeFence':
					if not in_question:
						raise Exception('\'\`\`\`\' code block should be inside \'@question\'')
					pass
#					 Send doc.rawText to code script runner and re-render the result
#					 Example code:
#					 print(doc.language)
#					 print(doc.rawText)
#					 result = runcode(doc.rawText, doc.language)
#					 self.question += renderer.render(Document(result))
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
			self.qtype = Qtypes.getQtype(doc.content)
			if self.qtype < 0:
				raise Exception(doc.content + ' is not a correct question type.')
		elif doc.option == 'feedback':
			self.feedback = doc.content
			
			
	def setAnswer(self, doc):
		"""
		Unwrap parsed MD and populate an answer
		"""
#		  Question type code
#		 'multiple choice': 1,
#		 'multiple answer': 2,
#		 'numerical': 3,
#		 'formula': 4,
#		 'essay': 5,
#		 'blank': 6,
#		 'multiple blank': 7,
#		 'matching': 8,
#		 'multiple dropdown': 9,
#		 'file': 10,
#		 'text': 11
		if self.qtype == 1 or self.qtype == 2 or self.qtype == 6: # multiple choice/answer, blank
			if doc.__class__.__name__ == 'List':
				for item in doc.children:
					self.answers.append(MultipleChoice(item))
			else:
				raise Exception('Answer format is incorrect.')
		elif self.qtype == 3: # numerical
			if doc.__class__.__name__ == 'Quote':
				self.answers.append(Numerical(doc))
			else:
				raise Exception('Answer format is incorrect.')
		elif self.qtype == 4: # formula
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
				raise Exception('Answer format is incorrect.')
		elif self.qtype == 7 or self.qtype == 8 or self.qtype == 9: # matching, multiple blanks/dropdown
			if doc.__class__.__name__ == 'List' and doc.children[0].leader == '+':
				for key in doc.children:
					for item in key.children[1].children:
						self.answers.append(Matching(item, key.children[0]))
			else:
				raise Exception('Answer format is incorrect')
		elif self.qtype == 5 or self.qtype == 10 or self.qtype == 11: # essay, file, text
			raise Exception('Answer is not required for essay, file, text question-type')
	
			  
	def debug(self):
		"""
		Print all members for debug purpose
		"""
		print('title:', self.title)
		print('points:', self.points)
		print('qtype:', self.qtype)
		print('question:', self.question)
		for a in self.answers:
			a.debug()
		print('feedback:', self.feedback)
		
		
class MDGroup(Group):
	"""
	Questions can be populated in a group and randomly picked
	 * 'points per question' will overwrite the points of each question
	
	Attr:
		pick (int): The number of questions that will be picked
		ppq (int): Points Per Question
		questions (List[Question]): List of questions
	"""
	def __init__(self):
		self.pick = -1
		self.ppq = -1
		self.questions = []

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
			
			
class MDQuiz(Quiz):
	"""
	Holds all information of the quiz
	
	Attr:
		title (str): Quiz title
		desc (str): Quiz description
		questions (List): List of Group and Question. They are populated into one list to
						  follow the order of questions in MD file
	"""
	def __init__(self, filename):
		self.title = ''
		self.description = ''
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
					pass
					#  Send doc.rawText to code script runner and put the result back into the list
					#  Example code:
					#  print(doc.language)
					#  print(doc.rawText)
					#  result = run_code(doc.rawText, doc.language)
					#  newDocs = Document(result)
					#  document.children[i+1:i] = newDocs.children
				elif doc.__class__.__name__ == 'Setting' and doc.option == 'quiz title':
					self.setTitle(doc.content)
				elif doc.__class__.__name__ == 'Setting' and doc.option == 'quiz description':
					self.setDescription(doc.content)
				elif doc.__class__.__name__ == 'Setting' and doc.option == 'group' and doc.content  == 'start':
					in_group = True
					group = MDGroup()
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
						group.questions.append(MDQuestion(docs))
					else:
						self.questions.append(MDQuestion(docs))
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