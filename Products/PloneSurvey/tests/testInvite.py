#
# Test PloneSurvey survey invite
#
from base import PloneSurveyTestCase

class TestEmail(PloneSurveyTestCase):
    """Test email formatted and sent"""

    def afterSetUp(self):
        self.useMockMailHost()
        self.createAnonSurvey()
        s1 = getattr(self.folder, 's1')
        assert len(s1.getAuthenticatedRespondents()) == 0
        self.loadRespondents()

    def testEmailText(self):
        s1 = getattr(self.folder, 's1')
        s1.survey_send_invite(email='user1@here.com')
        messages = self.portal.MailHost.messages
        first_message = messages[0]
        assert first_message['To'] == None
        assert 'user1@here.com' in first_message['Message'].get_payload()
        assert 'Dear User One' in first_message['Message'].get_payload()

    def testLinkInEmail(self):
        s1 = getattr(self.folder, 's1')
        s1.survey_send_invite(email='user1@here.com')
        messages = self.portal.MailHost.messages
        first_message = messages[0]
        user = s1.getAuthenticatedRespondent('user1@here.com')
        expected_key = user['key']
        expected_string = 'key=' + expected_key
        assert 'login_form_bridge?email=user1@here.com' in first_message['Message'].get_payload()
        assert expected_string in first_message['Message'].get_payload()

class TestSendMethods(PloneSurveyTestCase):
    """Test send method"""

    def afterSetUp(self):
        self.useMockMailHost()
        self.createAnonSurvey()
        s1 = getattr(self.folder, 's1')
        self.loadRespondents()

    def testSingleSend(self):
        """Test send to one user"""
        s1 = getattr(self.folder, 's1')
        s1.sendSurveyInvite('user2@here.com')
        messages = self.portal.MailHost.messages
        assert len(messages) == 1
        respondents = s1.getAuthenticatedRespondents()
        assert len(respondents) == 2

    def testAllSend(self):
        """Test send to one user"""
        s1 = getattr(self.folder, 's1')
        s1.survey_send_invite(email='all')
        messages = self.portal.MailHost.messages
        assert len(messages) == 2
        respondents = s1.getAuthenticatedRespondents()
        assert len(respondents) == 2

    def testNotSentTwice(self):
        """Test can't send twice to same user"""
        s1 = getattr(self.folder, 's1')
        s1.sendSurveyInvite('user2@here.com')
        messages = self.portal.MailHost.messages
        assert len(messages) == 1
        s1.survey_send_invite(email='new')
        messages = self.portal.MailHost.messages
        assert len(messages) == 2, len(messages)

    def testReminderSentTwice(self):
        """Test reminder sent twice to same user"""
        s1 = getattr(self.folder, 's1')
        s1.sendSurveyInvite('user2@here.com')
        messages = self.portal.MailHost.messages
        assert len(messages) == 1
        s1.survey_send_invite(email='all')
        messages = self.portal.MailHost.messages
        assert len(messages) == 3, len(messages)

class TestRegisterSent(PloneSurveyTestCase):
    """Test send method registers a respondent as being sent an email"""

    def afterSetUp(self):
        self.useMockMailHost()
        self.createAnonSurvey()
        s1 = getattr(self.folder, 's1')
        self.loadRespondents()

    def testRegisterMethod(self):
        """Test the register method works correctly"""
        s1 = getattr(self.folder, 's1')
        respondent = s1.getAuthenticatedRespondent('user2@here.com')
        assert respondent.has_key('email_sent')
        assert respondent['email_sent'] == ''
        s1.registerRespondentSent('user2@here.com')
        respondent = s1.getAuthenticatedRespondent('user2@here.com')
        assert respondent.has_key('email_sent')
        assert len(respondent['email_sent']) > 0

    def testSingleSend(self):
        """Test send to one user registers email sent"""
        s1 = getattr(self.folder, 's1')
        s1.sendSurveyInvite('user2@here.com')
        respondent = s1.getAuthenticatedRespondent('user2@here.com')
        assert respondent.has_key('email_sent')
        assert len(respondent['email_sent']) > 0

class TestSentFrom(PloneSurveyTestCase):
    """Test email is sent from correct address"""

    def afterSetUp(self):
        self.useMockMailHost()
        self.createAnonSurvey()
        s1 = getattr(self.folder, 's1')
        self.loadRespondents()

    def testDefaultFrom(self):
        """Default should come from site admin"""
        s1 = getattr(self.folder, 's1')
        s1.sendSurveyInvite('user2@here.com')
        messages = self.portal.MailHost.messages
        assert 'From: "Portal Administrator" <postmaster@localhost>' in messages[0].get_payload()

    def testDefaultFrom(self):
        """Default should come from site admin"""
        s1 = getattr(self.folder, 's1')
        s1.setInviteFromName('Survey Manager')
        s1.setInviteFromEmail('survey@here.com')
        s1.sendSurveyInvite('user2@here.com')
        messages = self.portal.MailHost.messages
        assert 'From: "Survey Manager" <survey@here.com>' in messages[0].get_payload()

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestEmail))
    suite.addTest(makeSuite(TestSendMethods))
    suite.addTest(makeSuite(TestRegisterSent))
    suite.addTest(makeSuite(TestSentFrom))
    return suite
