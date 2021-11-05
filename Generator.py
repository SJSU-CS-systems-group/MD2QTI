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
        # multiple answer: 2,
        elif question.qtype == 2:
            multiple_answer(question, section)
        # numerical: 3,
        elif question.qtype == 3:
            numerical(question, section)
        # formula: 4,
        elif question.qtype == 4:
            formula(question, section)
        # essay: 5,
        elif question.qtype == 5:
            essay(question, section)
        # blank: 6,
        elif question.qtype == 6:
            fill_in_the_blank(question, section)
        # multiple blank: 7,
        elif question.qtype == 7:
            fill_in_multiple_blank(question, section)
        # 'matching': 8,
        elif question.qtype == 8:
            matching(question, section)
        # multiple dropdown: 9,
        elif question.qtype == 9:
            multiple_dropdown(question, section)
        # file: 10,
        elif question.qtype == 10:
            file_upload(question, section)
        # text: 11
        elif question.qtype == 11:
            text_only(question, section)
        else:
            raise Exception('Invalid question format!')
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
        itemfeedback = ET.SubElement(parentElement, 'itemfeedback', {'ident':'general_fb'})
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
            displayfeedback = ET.SubElement(respcondition, 'displayfeedback', {'linkrefid': answer.ident+'_fb',
                                                                               'feedbacktype': 'Response'})
    respcondition = ET.SubElement(resprocessing, 'respcondition', {'continue': 'No'})
    conditionvar = ET.SubElement(respcondition, 'conditionvar')
    varequal = ET.SubElement(conditionvar, 'varequal', {'respident': 'response1'})
    varequal.text = correctChoice
    setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Set', 'varname': 'SCORE'})
    setvar.text = '100'

    #feedback
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
            displayfeedback = ET.SubElement(respcondition, 'displayfeedback', {'linkrefid': answer.ident+'_fb',
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

    #feedback
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
    #feedback
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
        for j in range(len(values)-1):
            var = ET.SubElement(var_set, 'var', {'name': values[j][0]})
            var.text = str(values[j][1])
        answer = ET.SubElement(var_set, 'answer')
        answer.text = str(values[-1][1])

    #feedback
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
    response_label = ET.SubElement(render_fib, 'response_label', {'ident': 'answer1', 'rshuffle':'No'})

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
    #feedback
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
            displayfeedback = ET.SubElement(respcondition, 'displayfeedback', {'linkrefid': answer.ident+'_fb',
                                                                               'feedbacktype': 'Response'})
    respcondition = ET.SubElement(resprocessing, 'respcondition', {'continue': 'No'})
    conditionvar = ET.SubElement(respcondition, 'conditionvar')
    for answer in question.answers:
        varequal = ET.SubElement(conditionvar, 'varequal', {'respident': 'response1'})
        varequal.text = answer.val
    setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Set', 'varname': 'SCORE'})
    setvar.text = '100'

    #feedback
    setFeedback(question, item)


def fill_in_multiple_blank(question, parentElement):
    dividedScore = str(float(100/len(question.keys)))
    item = ET.SubElement(parentElement, 'item', {'ident': question.ident, 'title': question.title})
    # Item metadata
    setItemMetaData(question, item)

    # Presentation
    presentation = ET.SubElement(item, 'presentation')
    material = ET.SubElement(presentation, 'material')
    mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
    mattext.text = question.question

    for key in question.keys:
        response_lid = ET.SubElement(presentation, 'response_lid', {'ident': 'response_'+key})
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
            varequal = ET.SubElement(conditionvar, "varequal", {'respident': 'response_'+answer.key})
            varequal.text = answer.ident
            displayfeedback = ET.SubElement(respcondition, 'displayfeedback', {'linkrefid': answer.ident+'_fb',
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

    #feedback
    setFeedback(question, item)


def matching(question, parentElement):
    numberOfValidKeys = 0
    for key in question.keys:
        if key != 'DISTRACTOR':
            numberOfValidKeys += 1
    dividedScore = str(float(100/numberOfValidKeys))
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
        response_lid = ET.SubElement(presentation, 'response_lid', {'ident': 'response_'+str(keyIndex)})
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
        varequal = ET.SubElement(conditionvar, "varequal", {'respident': 'response_'+str(keyIndex)})
        varequal.text = question.matchingVal[keyIndex]
        setvar = ET.SubElement(respcondition, 'setvar', {'action': 'Add', 'varname': 'SCORE'})
        setvar.text = dividedScore
        if question.answers[keyIndex].feedback != '':
            respcondition = ET.SubElement(resprocessing, 'respcondition')
            conditionvar = ET.SubElement(respcondition, 'conditionvar')
            nottag = ET.SubElement(conditionvar, 'not')
            varequal = ET.SubElement(nottag, "varequal", {'respident': 'response_'+keyIndex})
            varequal.text = question.matchingVal[keyIndex]
            displayfeedback = ET.SubElement(respcondition, 'displayfeedback', {'linkrefid': str(keyIndex)+'_fb',
                                                                               'feedbacktype': 'Response'})

    #feedback
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
    dividedScore = str(float(100/len(question.keys)))
    item = ET.SubElement(parentElement, 'item', {'ident': question.ident, 'title': question.title})
    # Item metadata
    setItemMetaData(question, item)

    # Presentation
    presentation = ET.SubElement(item, 'presentation')
    material = ET.SubElement(presentation, 'material')
    mattext = ET.SubElement(material, 'mattext', {'texttype': 'text/html'})
    mattext.text = question.question

    for key in question.keys:
        response_lid = ET.SubElement(presentation, 'response_lid', {'ident': 'response_'+key})
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
            varequal = ET.SubElement(conditionvar, "varequal", {'respident': 'response_'+answer.key})
            varequal.text = answer.ident
            displayfeedback = ET.SubElement(respcondition, 'displayfeedback', {'linkrefid': answer.ident+'_fb',
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

    #feedback
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


