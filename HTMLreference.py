import xml.etree.ElementTree as ET

# Document information
data = ET.Element('questestinterop', {'xmlns': 'http://www.imsglobal.org/xsd/ims_qtiasiv1p2',
                                      'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                                      'xsi:schemaLocation': 'http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd'})
assessment = ET.SubElement(data, 'assessment', {'ident': 'text2qti_assessment_c2ea45b3798e61ba533da9bf7cf770b2c3cba68e48d7df5d739b1939e01a435e', 'title': 'Quiz'})

# QTI metadata
qtimetadata = ET.SubElement(assessment, 'qtimetadata')
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'cc_maxattempts'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = '1'

section = ET.SubElement(assessment, 'section', {'ident': 'root_section'})

# For loop to turn each question into an item
# Each question is in 3 parts: item metadata, presentation, resprocessing

# Multiple choice
item = ET.SubElement(section, 'item', {'ident': 'QUESTION_IDENTIFIER_1', 'title': 'Multiple Choice'})
# Item metadata
itemmetadata = ET.SubElement(item, 'itemmetadata')
qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'question_type'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = 'multiple_choice_question'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'points_possible'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = '1'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'original_answer_ids'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = 'asdf, qwer'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'assessment_question_identifierref'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = 'UNIQUE_QUESTION_REFERENCE_ID_1'
# Presentation
presentation = ET.SubElement(item, 'presentation')
material = ET.SubElement(presentation, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
mattext.text = 'THE QUESTION GOES HERE'
response_lid = ET.SubElement(presentation, 'response_lid', {'ident': 'response1', 'rcardinality': 'Single'})
render_choice = ET.SubElement(response_lid, 'render_choice')
response_label = ET.SubElement(render_choice, 'response_label', {'ident': 'asdf'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
mattext.text = 'CHOICE_1'
response_label = ET.SubElement(render_choice, 'response_label', {'ident': 'qwer'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
mattext.text = 'CHOICE_2'
#Response processing
resprocessing = ET.SubElement(item, 'resprocessing')
outcomes = ET.SubElement(resprocessing, 'outcomes')
decvar = ET.SubElement(outcomes, 'decvar', {'maxvalue': '100',
                                            'minvalue': '0',
                                            'varname': 'SCORE',
                                            'vartype': 'Decimal'})
respcondition = ET.SubElement(resprocessing, 'respcondition', {'continue': 'No'})
conditionvar = ET.SubElement(respcondition, 'conditionvar')
varequal = ET.SubElement(conditionvar, 'varequal', {'respident': 'response1'})
varequal.text = 'asdf'
setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Set', 'varname': 'SCORE'})
setvar.text = '100'


# True/False
item = ET.SubElement(section, 'item', {'ident': 'QUESTION_IDENTIFIER_2', 'title': 'True/False'})
# Item metadata
itemmetadata = ET.SubElement(item, 'itemmetadata')
qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'question_type'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = 'true_false_question'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'points_possible'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = '1.0'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'original_answer_ids'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = '8053, 4218'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'assessment_question_identifierref'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = 'UNIQUE_QUESTION_REFERENCE_ID_2'
# Presentation
presentation = ET.SubElement(item, 'presentation')
material = ET.SubElement(presentation, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
mattext.text = 'This is a true false question'
response_lid = ET.SubElement(presentation, 'response_lid', {'ident': 'response1', 'rcardinality': 'Single'})
render_choice = ET.SubElement(response_lid, 'render_choice')
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '8053'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
mattext.text = 'True'
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '4218'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
mattext.text = 'False'
#Response processing
resprocessing = ET.SubElement(item, 'resprocessing')
outcomes = ET.SubElement(resprocessing, 'outcomes')
decvar = ET.SubElement(outcomes, 'decvar', {'maxvalue': '100',
                                            'minvalue': '0',
                                            'varname': 'SCORE',
                                            'vartype': 'Decimal'})
respcondition = ET.SubElement(resprocessing, 'respcondition', {'continue': 'No'})
conditionvar = ET.SubElement(respcondition, 'conditionvar')
varequal = ET.SubElement(conditionvar, 'varequal', {'respident': 'response1'})
varequal.text = '8053'
setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Set', 'varname': 'SCORE'})
setvar.text = '100'


# Fill in the Blank
item = ET.SubElement(section, 'item', {'ident': 'QUESTION_IDENTIFIER_3', 'title': 'Fill In the Blank'})
# Item metadata
itemmetadata = ET.SubElement(item, 'itemmetadata')
qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'question_type'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = 'short_answer_question'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'points_possible'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = '1.0'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'original_answer_ids'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = '618'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'assessment_question_identifierref'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = 'UNIQUE_QUESTION_REFERENCE_ID_3'
# Presentation
presentation = ET.SubElement(item, 'presentation')
material = ET.SubElement(presentation, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
mattext.text = 'Type ANSWER A'
response_str = ET.SubElement(presentation, 'response_str', {'ident': 'response1', 'rcardinality': 'Single'})
render_fib = ET.SubElement(response_str, 'render_fib')
response_label = ET.SubElement(render_fib, 'response_label', {'ident': 'answer1', 'rshuffle':'No'})
#Response processing
resprocessing = ET.SubElement(item, 'resprocessing')
outcomes = ET.SubElement(resprocessing, 'outcomes')
decvar = ET.SubElement(outcomes, 'decvar', {'maxvalue': '100',
                                            'minvalue': '0',
                                            'varname': 'SCORE',
                                            'vartype': 'Decimal'})
respcondition = ET.SubElement(resprocessing, 'respcondition', {'continue': 'No'})
conditionvar = ET.SubElement(respcondition, 'conditionvar')
varequal = ET.SubElement(conditionvar, 'varequal', {'respident': 'response1'})
varequal.text = 'ANSWER A'
setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Set', 'varname': 'SCORE'})
setvar.text = '100'


# Fill in the Multiple Blank
item = ET.SubElement(section, 'item', {'ident': 'QUESTION_IDENTIFIER_4', 'title': 'Fill In Multiple Blank'})
# Item metadata
itemmetadata = ET.SubElement(item, 'itemmetadata')
qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'question_type'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = 'fill_in_multiple_blanks_question'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'points_possible'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = '1.0'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'original_answer_ids'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = '302,3485'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'assessment_question_identifierref'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = 'UNIQUE_QUESTION_REFERENCE_ID_4'
# Presentation
presentation = ET.SubElement(item, 'presentation')
material = ET.SubElement(presentation, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
mattext.text = 'Choice A goes here [choiceA], and Choice B goes here [choiceB].'
response_lid = ET.SubElement(presentation, 'response_lid', {'ident': 'response_choiceA'})
material = ET.SubElement(response_lid, 'material')
mattext = ET.SubElement(material, 'mattext')
mattext.text = 'choiceA'
render_choice = ET.SubElement(response_lid, 'render_choice')
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '302'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
mattext.text = 'Choice A'
response_lid = ET.SubElement(presentation, 'response_lid', {'ident': 'response_choiceB'})
material = ET.SubElement(response_lid, 'material')
mattext = ET.SubElement(material, 'mattext')
mattext.text = 'choiceB'
render_choice = ET.SubElement(response_lid, 'render_choice')
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '3485'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
mattext.text = 'Choice B'
#Response processing
resprocessing = ET.SubElement(item, 'resprocessing')
outcomes = ET.SubElement(resprocessing, 'outcomes')
decvar = ET.SubElement(outcomes, 'decvar', {'maxvalue': '100',
                                            'minvalue': '0',
                                            'varname': 'SCORE',
                                            'vartype': 'Decimal'})
respcondition = ET.SubElement(resprocessing, 'respcondition')
conditionvar = ET.SubElement(respcondition, 'conditionvar')
varequal = ET.SubElement(conditionvar, 'varequal', {'respident': 'response_choiceA'})
varequal.text = '302'
setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Add', 'varname': 'SCORE'})
setvar.text = '50.00'
respcondition = ET.SubElement(resprocessing, 'respcondition')
conditionvar = ET.SubElement(respcondition, 'conditionvar')
varequal = ET.SubElement(conditionvar, 'varequal', {'respident': 'response_choiceB'})
varequal.text = '3485'
setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Add', 'varname': 'SCORE'})
setvar.text = '50.00'


# Multiple Answers
item = ET.SubElement(section, 'item', {'ident': 'QUESTION_IDENTIFIER_5', 'title': 'Multiple Answers'})
# Item metadata
itemmetadata = ET.SubElement(item, 'itemmetadata')
qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'question_type'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = 'multiple_answers_questions'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'points_possible'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = '1.0'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'original_answer_ids'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = '4834,6679,4154'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'assessment_question_identifierref'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = 'UNIQUE_QUESTION_REFERENCE_ID_5'
# Presentation
presentation = ET.SubElement(item, 'presentation')
material = ET.SubElement(presentation, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
mattext.text = 'This is a multiple answers question.'
response_lid = ET.SubElement(presentation, 'response_lid', {'ident': 'response1', 'rcardinality':'Multiple'})
render_choice = ET.SubElement(response_lid, 'render_choice')
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '4834'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype':'text/plain'})
mattext.text = 'Choice A'
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '6679'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype':'text/plain'})
mattext.text = 'Choice B'
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '4154'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype':'text/plain'})
mattext.text = 'Choice C'
#Response processing
resprocessing = ET.SubElement(item, 'resprocessing')
outcomes = ET.SubElement(resprocessing, 'outcomes')
decvar = ET.SubElement(outcomes, 'decvar', {'maxvalue': '100',
                                            'minvalue': '0',
                                            'varname': 'SCORE',
                                            'vartype': 'Decimal'})
respcondition = ET.SubElement(resprocessing, 'respcondition', {'continue':'No'})
conditionvar = ET.SubElement(respcondition, 'conditionvar')
and_ = ET.SubElement(conditionvar, 'and')
varequal = ET.SubElement(and_, 'varequal', {'respident': 'response1'})
varequal.text = '4834'
not_= ET.SubElement(and_, 'not')
varequal = ET.SubElement(not_, 'varequal', {'respident': 'response1'})
varequal.text = '6679'
not_= ET.SubElement(and_, 'not')
varequal = ET.SubElement(not_, 'varequal', {'respident': 'response1'})
varequal.text = '4154'
setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Add', 'varname': 'SCORE'})
setvar.text = '100'


# Multiple Dropdowns
item = ET.SubElement(section, 'item', {'ident': 'QUESTION_IDENTIFIER_6', 'title': 'Multiple Dropdowns'})
# Item metadata
itemmetadata = ET.SubElement(item, 'itemmetadata')
qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'question_type'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = 'multiple_dropdowns_questions'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'points_possible'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = '1.0'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'original_answer_ids'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = '6365,3542,8435,8425,687,1481'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'assessment_question_identifierref'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = 'UNIQUE_QUESTION_REFERENCE_ID_6'
# Presentation
presentation = ET.SubElement(item, 'presentation')
material = ET.SubElement(presentation, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
mattext.text = 'Pick choice A here [choiceA], and pick choice B here [choiceB].'
response_lid = ET.SubElement(presentation, 'response_lid', {'ident': 'response_choiceA'})
material = ET.SubElement(response_lid, 'material')
mattext = ET.SubElement(material, 'mattext')
mattext.text = 'ChoiceA'
render_choice = ET.SubElement(response_lid, 'render_choice')
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '6365'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype':'text/plain'})
mattext.text = 'Choice A'
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '3542'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype':'text/plain'})
mattext.text = 'Choice B'
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '8435'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype':'text/plain'})
mattext.text = 'Choice C'
response_lid = ET.SubElement(presentation, 'response_lid', {'ident': 'response_choiceB'})
material = ET.SubElement(response_lid, 'material')
mattext = ET.SubElement(material, 'mattext')
mattext.text = 'ChoiceB'
render_choice = ET.SubElement(response_lid, 'render_choice')
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '8425'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype':'text/plain'})
mattext.text = 'Choice A'
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '687'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype':'text/plain'})
mattext.text = 'Choice B'
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '1481'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype':'text/plain'})
mattext.text = 'Choice C'
#Response processing
resprocessing = ET.SubElement(item, 'resprocessing')
outcomes = ET.SubElement(resprocessing, 'outcomes')
decvar = ET.SubElement(outcomes, 'decvar', {'maxvalue': '100',
                                            'minvalue': '0',
                                            'varname': 'SCORE',
                                            'vartype': 'Decimal'})
respcondition = ET.SubElement(resprocessing, 'respcondition')
conditionvar = ET.SubElement(respcondition, 'conditionvar')
varequal = ET.SubElement(conditionvar, 'varequal', {'respident':'response_choiceA'})
varequal.text = '6365'
setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Add', 'varname': 'SCORE'})
setvar.text = '50.00'
respcondition = ET.SubElement(resprocessing, 'respcondition')
conditionvar = ET.SubElement(respcondition, 'conditionvar')
varequal = ET.SubElement(conditionvar, 'varequal', {'respident':'response_choiceB'})
varequal.text = '687'
setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Add', 'varname': 'SCORE'})
setvar.text = '50.00'


# Matching
item = ET.SubElement(section, 'item', {'ident': 'QUESTION_IDENTIFIER_7', 'title': 'Matching'})
# Item metadata
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
fieldentry.text = '1.0'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'original_answer_ids'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = '4495,1274,8354'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'assessment_question_identifierref'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = 'UNIQUE_QUESTION_REFERENCE_ID_7'
# Presentation
presentation = ET.SubElement(item, 'presentation')
material = ET.SubElement(presentation, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
mattext.text = 'This is a matching question'
response_lid = ET.SubElement(presentation, 'response_lid', {'ident': 'response_4495'})
material = ET.SubElement(response_lid, 'material')
mattext = ET.SubElement(material, 'mattext',{'texttype':'text/plain'})
mattext.text = 'Choice 1'
render_choice = ET.SubElement(response_lid, 'render_choice')
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '7381'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext')
mattext.text = 'Choice A'
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '239'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext')
mattext.text = 'Choice B'
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '1793'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext')
mattext.text = 'Choice C'
response_lid = ET.SubElement(presentation, 'response_lid', {'ident': 'response_1274'})
material = ET.SubElement(response_lid, 'material')
mattext = ET.SubElement(material, 'mattext',{'texttype':'text/plain'})
mattext.text = 'Choice 2'
render_choice = ET.SubElement(response_lid, 'render_choice')
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '7381'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext')
mattext.text = 'Choice A'
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '239'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext')
mattext.text = 'Choice B'
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '1793'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext')
mattext.text = 'Choice C'
response_lid = ET.SubElement(presentation, 'response_lid', {'ident': 'response_8354'})
material = ET.SubElement(response_lid, 'material')
mattext = ET.SubElement(material, 'mattext',{'texttype':'text/plain'})
mattext.text = 'Choice 3'
render_choice = ET.SubElement(response_lid, 'render_choice')
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '7381'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext')
mattext.text = 'Choice A'
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '239'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext')
mattext.text = 'Choice B'
response_label = ET.SubElement(render_choice, 'response_label', {'ident': '1793'})
material = ET.SubElement(response_label, 'material')
mattext = ET.SubElement(material, 'mattext')
mattext.text = 'Choice C'
#Response processing
resprocessing = ET.SubElement(item, 'resprocessing')
outcomes = ET.SubElement(resprocessing, 'outcomes')
decvar = ET.SubElement(outcomes, 'decvar', {'maxvalue': '100',
                                            'minvalue': '0',
                                            'varname': 'SCORE',
                                            'vartype': 'Decimal'})
respcondition = ET.SubElement(resprocessing, 'respcondition')
conditionvar = ET.SubElement(respcondition, 'conditionvar')
varequal = ET.SubElement(conditionvar, 'varequal', {'respident':'response_4495'})
varequal.text = '7381'
setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Add', 'varname': 'SCORE'})
setvar.text = '33.33'
respcondition = ET.SubElement(resprocessing, 'respcondition')
conditionvar = ET.SubElement(respcondition, 'conditionvar')
varequal = ET.SubElement(conditionvar, 'varequal', {'respident':'response_1274'})
varequal.text = '239'
setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Add', 'varname': 'SCORE'})
setvar.text = '33.33'
respcondition = ET.SubElement(resprocessing, 'respcondition')
conditionvar = ET.SubElement(respcondition, 'conditionvar')
varequal = ET.SubElement(conditionvar, 'varequal', {'respident':'response_8354'})
varequal.text = '1793'
setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Add', 'varname': 'SCORE'})
setvar.text = '33.33'


# File Upload Question
item = ET.SubElement(section, 'item', {'ident': 'QUESTION_IDENTIFIER_10', 'title': 'File Upload Question'})
# Item metadata
itemmetadata = ET.SubElement(item, 'itemmetadata')
qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'question_type'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = 'file_upload_question'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'points_possible'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = '1.0'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'original_answer_ids'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'assessment_question_identifierref'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = 'UNIQUE_QUESTION_REFERENCE_ID_10'
# Presentation
presentation = ET.SubElement(item, 'presentation')
material = ET.SubElement(presentation, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
mattext.text = 'This is a file upload question'
#Response processing
resprocessing = ET.SubElement(item, 'resprocessing')
outcomes = ET.SubElement(resprocessing, 'outcomes')
decvar = ET.SubElement(outcomes, 'decvar', {'maxvalue': '100',
                                            'minvalue': '0',
                                            'varname': 'SCORE',
                                            'vartype': 'Decimal'})


# Text Question
item = ET.SubElement(section, 'item', {'ident': 'QUESTION_IDENTIFIER_11', 'title': 'Text'})
# Item metadata
itemmetadata = ET.SubElement(item, 'itemmetadata')
qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'question_type'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = 'text_only_question'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'points_possible'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = '0'
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'original_answer_ids'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'assessment_question_identifierref'
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = 'UNIQUE_QUESTION_REFERENCE_ID_11'
# Presentation
presentation = ET.SubElement(item, 'presentation')
material = ET.SubElement(presentation, 'material')
mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
mattext.text = 'This is just text.'
#No Response processing


mydata = ET.tostring(data)
myfile = open("sample/test.xml", "wb")
myfile.write(mydata)
