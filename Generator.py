import xml.etree.ElementTree as ET
from MDQuiz import MDQuiz


def Generator(MDQuiz):
    # Document information
    data = ET.Element('questestinterop', {'xmlns': 'http://www.imsglobal.org/xsd/ims_qtiasiv1p2',
                                          'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                                          'xsi:schemaLocation': 'http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd'})
    assessment = ET.SubElement(data, 'assessment', {
        'ident': 'text2qti_assessment_c2ea45b3798e61ba533da9bf7cf770b2c3cba68e48d7df5d739b1939e01a435e',
        'title': 'Quiz'})
    # QTI metadata
    qtimetadata = ET.SubElement(assessment, 'qtimetadata')
    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
    fieldlabel.text = 'cc_maxattempts'
    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
    fieldentry.text = '1'

    section = ET.SubElement(assessment, 'section', {'ident': 'root_section'})

    #For loop through MDQuiz.questions
    return data


def MC(question):
    return 1