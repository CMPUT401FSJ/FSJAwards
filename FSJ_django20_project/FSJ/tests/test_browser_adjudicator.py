from ..models import *
from django.contrib.auth.models import User
from selenium.webdriver.support.wait import WebDriverWait
timeout = 15
import time
import pytz
import datetime
from datetime import date
from .selenium_test import SeleniumTest
from django.conf import settings
from selenium.webdriver.firefox.webdriver import WebDriver


class AdjudicatorSeleniumTest(SeleniumTest):

    @classmethod
    def setUpClass(cls):
        super(AdjudicatorSeleniumTest, cls).setUpClass()


    def setUp(self):
        self.password = "adj_password"
        self.ccid = "adjudicator"
        self.first_name = "An"
        self.last_name = "Adjudicator"
        self.email = "adjudicator@csjawards.ca"
        self.lang_pref = "en"

        self.user = User.objects.create_user(username=self.ccid,
                                            password=self.password)

        self.adjudicator = Adjudicator.objects.create(ccid=self.ccid, first_name=self.first_name,
                                                     last_name=self.last_name, email=self.email,
                                                     user=self.user, lang_pref=self.lang_pref)

        self.user = User.objects.get(username=self.ccid)

        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id("id_username"))

        username = self.selenium.find_element_by_id("id_username")
        username.send_keys(self.ccid)

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id("id_password"))

        password =self.selenium.find_element_by_id("id_password")
        password.send_keys(self.password)

        save = self.selenium.find_element_by_css_selector("button.btn:nth-child(5)")
        save.click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))


    def tearDown(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/logout/'))

    def test_adjudicator_awards(self):
        self.award_name = "An Award Name"
        self.award_description = "An Award Description"
        self.award_value = "An Award Value"
        self.award_start_date = datetime.datetime.now(pytz.timezone('America/Vancouver'))
        self.award_end_date = datetime.datetime.now(pytz.timezone('America/Edmonton'))
        self.award_documents_needed = False
        self.award_is_active = True

        self.student_ccid = "student"
        self.student_password = "stud_password"
        self.student_first_name = "A"
        self.student_last_name = "Student"
        self.student_email = "student@csjawards.ca"
        self.student_lang_pref = "en"
        self.student_id = "123456789"
        self.program_name = "A Program Name"
        self.program_code = "A Code"
        self.year_name = "Year 1"
        self.program = Program.objects.create(name=self.program_name, code=self.program_code)
        self.year = YearOfStudy.objects.create(year=self.year_name)

        self.award = Award.objects.create(name=self.award_name, description=self.award_description,
                                          value=self.award_value,
                                          start_date=self.award_start_date, end_date=self.award_end_date,
                                          documents_needed=self.award_documents_needed, is_active=self.award_is_active)


        self.student_user = User.objects.create_user(username=self.student_ccid,
                                             password=self.student_password)

        self.student = Student.objects.create(ccid=self.student_ccid, first_name=self.student_first_name,
                                              last_name=self.student_last_name, email=self.student_email,
                                              user=self.student_user, lang_pref=self.student_lang_pref,
                                              student_id=self.student_id, program=self.program,
                                              year=self.year)

        self.application = Application.objects.create(student = self.student, award = self.award, is_submitted=True)


        self.committee_name = "A Committee"

        self.committee = Committee.objects.create(committee_name=self.committee_name)
        self.committee.awards.add(self.award)
        self.committee.adjudicators.add(self.adjudicator)
        self.committee.save()

        self.selenium.get('%s%s' % (self.live_server_url, '/awards/'))

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))


        self.selenium.find_element_by_link_text(self.committee_name).click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_link_text("Review Required"))

        time.sleep(5)

        self.selenium.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[2]/div/div[2]/table/tbody/tr[2]/td[7]/a").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        self.selenium.find_element_by_link_text("View Application").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))


        self.comment_text = "A comment"
        self.ranking = 1

        self.selenium.find_element_by_id("id_form-comment_text").send_keys(self.comment_text)
        self.selenium.find_element_by_css_selector("#id_form2-rank > option:nth-child(2)").click()
        self.selenium.find_element_by_css_selector("button.btn.btn-success").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        comment = Comment.objects.get(application=self.application, adjudicator=self.adjudicator)
        self.assertEquals(self.comment_text, comment.comment_text)

        ranking = Ranking.objects.get(application=self.application, adjudicator=self.adjudicator)
        self.assertEquals(self.ranking, ranking.rank)

        self.selenium.find_element_by_link_text("Review Completed").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        self.new_comment_text = "A new comment"
        self.new_ranking = 2

        self.selenium.find_element_by_id("id_form-comment_text").clear()
        self.selenium.find_element_by_id("id_form-comment_text").send_keys(self.new_comment_text)
        self.selenium.find_element_by_css_selector("#id_form2-rank > option:nth-child(3)").click()
        self.selenium.find_element_by_css_selector("button.btn.btn-success").click()

        comment = Comment.objects.get(application=self.application, adjudicator=self.adjudicator)
        self.assertEquals(self.new_comment_text, comment.comment_text)

        ranking = Ranking.objects.get(application=self.application, adjudicator=self.adjudicator)
        self.assertEquals(self.new_ranking, ranking.rank)


