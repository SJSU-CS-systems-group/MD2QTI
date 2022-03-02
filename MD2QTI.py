import os
from zipfile import ZipFile
import shutil
from QuizGenerator import Generator
from IMSGenerator import IMSContent
from MetaGenerator import MetadataContent
from Parser import *
import sys
import mistletoe
from mistletoe import Document
import xml.etree.ElementTree as ET


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
