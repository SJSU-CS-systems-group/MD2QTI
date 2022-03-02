import xml.etree.ElementTree as ET


def MetadataContent(quizData):
    # Metadata information
    data = ET.Element('quiz',{'xsi:schemaLocation': 'http://canvas.instructure.om/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd',
                              'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                              'xmlns': 'http//canvas.instructure.com/xsd/cccv1p0',
                              'identifer': 'md2qti_assessment_'+quizData.ident})

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
    quizident.text = 'md2qti_assessment_'+quizData.ident
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
