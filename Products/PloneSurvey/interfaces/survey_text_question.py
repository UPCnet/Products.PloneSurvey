from zope.interface import Interface, Attribute

class ISurveyTextQuestion(Interface):
    """A textual question within a survey"""

    def getValidators():
        """Return a list of validators"""

    def validateQuestion(value):
        """Return a list of validators"""
