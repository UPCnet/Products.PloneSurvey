## Script (Python) "scomponi"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=carattere='§'
##title=
##
#carattere = '§'

sep = carattere + ',' + carattere
def fai_stringa(vett):
 vett1 = []
 for v in vett:
  vett1.append(v.replace('"','""'))
 return carattere + sep.join(vett1) + carattere


file = context.buildSpreadsheetUrl()
setHeader = context.REQUEST.RESPONSE.setHeader
setHeader('Content-Type','application/vnd.ms-excel')
setHeader('Content-disposition','attachment; filename=%s' % file)
if 1 == 1:
        tabella = {}
        questions = context.getAllQuestionsInOrder()
        domande = [q.Title() for q in questions]
        domande = []
        for q in questions:
         if q.meta_type == "SurveyMatrixQuestion" and q.getInputType() not in ['radio', 'checkbox']:
          for opt in q.getQuestionOptions():
           domande.append(q.getId() + "-" + opt)
         else:
          domande.append(q.Title())
        print fai_stringa(["user"] + domande + ["completed"])

        for user in context.getRespondents():
            if context.getConfidential():
                row = ['Anonymous']
            else:
                row = [context.getRespondentFullName(user) or user]
            for question in questions:
                answer = question.getAnswerFor(user) or ''
                if question.meta_type == "SurveyMatrixQuestion":
                 lunghezza_campo = len(question.getQuestionOptions())
                 if answer <> None:
                  if (same_type(answer, []) or same_type(answer, ())) and question.getInputType() not in ['radio', 'checkbox']:
                   for i in range(0, lunghezza_campo):
                    try:
                     row.append(str(answer[i]))
                    except:
                     row.append('')
                  else:
                    row.append(str(answer))
                 else:
                  for opt in question.getQuestionOptions():
                    row.append('Non prevista')
                else:
                 if question.meta_type == "SurveyGridQuestion":
                  if question.getId() + ' - ' + question.Title() not in tabella.keys():
                   tabella[question.getId() + ' - ' + question.Title()] = []
                  columns = question.getAllColumns()
                  for i in answer:
                    linea = [ (context.getRespondentFullName(user) or user) ]
                    for column in columns:
		      if column in i.keys():
                       linea.append(i[column])
		      else:
		       linea.append('vuoto')
                    tabella[question.getId() + ' - ' + question.Title()].append(fai_stringa(linea))
                  row.append('')
                 else:
                  row.append(str(answer))

            row.append(context.checkCompletedFor(user) and 'Completed' or 'Not Completed')
            print fai_stringa(row)

        for k in tabella.keys():
         print carattere + k + carattere
         for t in tabella[k]:
          print t

        return printed

