from AccessControl import ClassSecurityInfo
from zope.interface import implements

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import registerATCT
from Products.validation import validation

from Products.PloneSurvey import permissions
from Products.PloneSurvey.config import PROJECTNAME
from Products.PloneSurvey.config import TEXT_VALIDATORS
from Products.PloneSurvey.content.BaseQuestion import BaseQuestion
from Products.PloneSurvey.interfaces import IPloneSurveyQuestion
from Products.PloneSurvey.interfaces import ISurveyTextQuestion

from schemata import SurveyTextQuestionSchema

class SurveyTextQuestion(BaseQuestion):
    """A textual question within a survey"""
    schema = SurveyTextQuestionSchema
    portal_type = 'Survey Text Question'
    _at_rename_after_creation = True

    implements(IPloneSurveyQuestion, ISurveyTextQuestion)

    security = ClassSecurityInfo()

    security.declareProtected(permissions.View, 'validateAnswer')
    def validateAnswer(self, value, state):
        """Validate the question"""
        if len(value) > self.getMaxLength():
            state.setError(self.getId(), "Answer too long, must be less than %s characters" % self.getMaxLength())
        else:
            self.addAnswer(value)

    security.declareProtected(permissions.View, 'getValidators')
    def getValidators(self):
        """Return a list of validators"""
        validator_list = ['None', ]
        validator_list.extend(TEXT_VALIDATORS)
        return validator_list

    security.declareProtected(permissions.View, 'validateQuestion')
    def validateQuestion(self, value):
        """Return a list of validators"""
        validator = self.getValidation()
        v = validation.validatorFor(validator)
        return v(value)

registerATCT(SurveyTextQuestion, PROJECTNAME)
