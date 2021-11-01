import xml.etree.ElementTree as ET
from Parser import ParsedQuiz


def Generator(MDQuiz):
    # Document information
    data = ET.Element('questestinterop', {'xmlns': 'http://www.imsglobal.org/xsd/ims_qtiasiv1p2',
                                          'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                                          'xsi:schemaLocation': 'http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd'})
    assessment = ET.SubElement(data, 'assessment', {
        'ident': MDQuiz.ident,
        'title': MDQuiz.title})
    # # QTI metadata
    # qtimetadata = ET.SubElement(assessment, 'qtimetadata')
    # qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
    # fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
    # fieldlabel.text = 'cc_maxattempts'
    # fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
    # fieldentry.text = '1'
    #
    section = ET.SubElement(assessment, 'section', {'ident': 'root_section'})

    #For loop through MDQuiz.questions

    for question in MDQuiz.questions:
        # multiple choice: 1,
        if question.qtype == 1:
            multiple_choice(question, section)
        # 'multiple answer': 2,
        # elif question.qtype == 2:
        #     multiple_answer(question, data)
        # # 'numerical': 3,
        # # elif question.qtype == 3:
        #     # numerical(question, data)
        # # 'formula': 4,
        # elif question.qtype == 4:
        # # 'essay': 5,
        # elif question.qtype == 5:
        # # 'blank': 6,
        # elif question.qtype == 6:
        #     blank(question, data)
        # # 'multiple blank': 7,
        # elif question.qtype == 7:
        #     multiple_blank(question, data)
        # # 'matching': 8,
        # elif question.qtype == 8:
        #     matching(question, data)
        # # 'multiple dropdown': 9,
        # elif question.qtype == 9:
        #     multiple_dropdown(question, data)
        # 'file': 10,
        # 'text': 11
        else:
            itemMetadata = ET.SubElement(section, 'asdfadfasfafasdfaf')
    return data


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
        respcondition = ET.SubElement(resprocessing, 'respcondition', {'continue': 'Yes'})
        conditionvar = ET.SubElement(respcondition, "conditionvar")
        other = ET.SubElement(conditionvar, "other")
        displayfeedback = ET.SubElement(respcondition, 'displayfeedback', {'linkrefid': 'general_fb',
                                                                           'feedbacktype': 'Response'})
    for answer in question.answers:
        if answer.is_correct:
            correctChoice = answer.ident
        if answer.feedback != '':
            respcondition = ET.SubElement(resprocessing, 'respcondition', {'continue': 'Yes'})
            conditionvar = ET.SubElement(respcondition, "conditionvar")
            varequal = ET.SubElement(conditionvar, "varequal", {'respident': 'response1'})
            varequal.text = answer.ident
            displayfeedback = ET.SubElement(respcondition, 'displayfeedback', {'linkrefid': answer.ident+'_fb',
                                                                               'feedbacktype': 'Response'})
    respcondition = ET.SubElement(resprocessing, 'respcondition', {'continue': 'No'})
    conditionvar = ET.SubElement(respcondition, 'conditionvar')
    varequal = ET.SubElement(conditionvar, 'varequal', {'respident': 'response1'})
    varequal.text = correctChoice
    setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Set', 'varname': 'SCORE'})
    setvar.text = '100'
    if question.feedback != '':
        itemfeedback = ET.SubElement(item, 'itemfeedback', {'ident':'general_fb'})
        flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
        material = ET.SubElement(flow_mat, 'material')
        mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
        mattext.text = question.feedback
    for answer in question.answers:
        if answer.feedback != '':
            itemfeedback = ET.SubElement(item, 'itemfeedback', {'ident': answer.ident + '_fb'})
            flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
            material = ET.SubElement(flow_mat, 'material')
            mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
            mattext.text = answer.feedback