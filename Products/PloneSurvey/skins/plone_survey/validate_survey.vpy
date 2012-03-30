form = context.REQUEST.form
_ = context.translate
questions = context.getQuestions()

if form.get('form.button.save', ''):
    # skip validation
    for q in questions:
        value = form.get(q.getId(), '')
        comments = form.get("%s_comments" % q.getId(), '')
        if q.portal_type == 'SurveySelectQuestion' and q.getLikertOptions():
            q.addAnswer(int(value), comments)
        elif q.portal_type not in ('SurveyMatrix', 'SurveyTwoDimensional'):
            q.addAnswer(value, comments)
        else:
            matrix_questions = q.getQuestions()
            for matrix_q in matrix_questions:
                value = form.get(q.getId() + '-' + matrix_q.getId(), '')
                matrix_q.addAnswer(value)
    return state.set(status='success')

for q in questions:
    value = form.get(q.getId(), '')
    if q.portal_type == 'SurveyMatrix':
        pass
    elif q.getRequired() and not value and (q.portal_type not in ['SurveyTwoDimensional', 'SurveyDateQuestion']):
        error_msg = _(msgid='please_provide_answer',
            default=u'Please provide an answer for this question',
            domain='plonesurvey')
        state.setError(q.getId(), error_msg)
    if value and hasattr(q, 'getValidation') and q.getValidation() != 'None':
        validation_output = q.validateQuestion(value)
        if validation_output != 1:
            state.setError(q.getId(), validation_output)
    comments = form.get("%s_comments" % q.getId(), '')
    if q.portal_type == 'SurveyTextQuestion':
        q.validateAnswer(value, state)
    elif q.portal_type == 'SurveyDateQuestion':
        q.validateAnswer(form, q.getId(), state)
    elif q.portal_type == 'SurveySelectQuestion':
        q.validateAnswer(value, comments, state)
    elif q.portal_type not in ('SurveyMatrix', 'SurveyTwoDimensional'):
        q.addAnswer(value, comments)
    elif q.portal_type in ('SurveyMatrix',):
        q.validateAnswer(form, state)
    elif q.portal_type in ('SurveyMatrix', 'SurveyTwoDimensional'):
        matrix_questions = q.getQuestions()
        qnum = ''
        for matrix_q in matrix_questions:
            matrix_qid = str(q.getId()) + '-' + str(matrix_q.getId())
            value = form.get(matrix_qid, '')
            try:
                value = int(value)
            except TypeError:
                # most probably we have multiple selects
                newvalue = []
                for number in value:
                    try:
                        newvalue.append(int(number))
                    except ValueError:
                        newvalue.append(number)
                value = newvalue
            except ValueError:
                pass
            if matrix_q.getRequired() and not value:
               qnum = qnum + ' ' + str(matrix_q.title_or_id()) + ','
            matrix_q.addAnswer(value)
        if qnum != '':
            qnum = qnum[:-1]
            error_msg = _(msgid='please_provide_answer',
                default=u'Please provide an answer for this question',
                domain='plonesurvey')
            state.setError(q.getId(), "%s %s" % (error_msg, qnum))

if not state.getErrors():
    if context.getShowCaptcha():
        if context.portal_quickinstaller.isProductInstalled('quintagroup.plonecaptchas'):
            context.captcha_validator()
    
if state.getErrors():
    return state.set(status='failure', portal_status_message=_(msgid='text_correct_errors',
                                                               default=u'Please correct the errors shown',
                                                               domain='plonesurvey'))
else:
    state.set(status='success')
    state.setKwargs({'survey_user_id':form.get('survey_user_id')})
    return state
return state
