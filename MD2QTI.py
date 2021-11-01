from Generator import Generator
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
	mdquiz = ParsedQuiz(filename)  # Parse the file into metadata
	# generate qti data from metadata
	# write back to QTI file
	data = Generator(mdquiz)
	mydata = ET.tostring(data)
	myfile = open("sample/test.xml", "wb")
	myfile.write(mydata)

	mdquiz.debug()
	for q in mdquiz.questions:
		if q.__class__.__name__ == 'MDGroup':
			print('--group-start--')
			print('points per question:', q.ppq)
			print('pick:', q.pick)
			for q2 in q.questions:
				q2.debug()
			print('--group-end--')
		else:
			q.debug()
			print('')
