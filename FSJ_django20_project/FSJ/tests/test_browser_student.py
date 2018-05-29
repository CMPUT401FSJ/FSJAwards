from ..models import *
from django.contrib.auth.models import User
from selenium.webdriver.support.wait import WebDriverWait
timeout = 15
import pytz
import datetime
from datetime import date
from .selenium_test import SeleniumTest
from django.conf import settings
import re


class StudentSeleniumTest(SeleniumTest):

    @classmethod
    def setUpClass(cls):
        super(StudentSeleniumTest, cls).setUpClass()


    def setUp(self):
        self.password = "stud_password"
        self.ccid = "student"
        self.first_name = "A"
        self.last_name = "Student"
        self.email = "student@csjawards.ca"
        self.lang_pref = "en"
        self.student_id = "123456789"
        self.program_name = "A Program Name"
        self.program_code = "A Code"
        self.year_name = "Year 1"
        self.program = Program.objects.create(name=self.program_name, code=self.program_code)
        self.year = YearOfStudy.objects.create(year=self.year_name)


        self.user = User.objects.create_user(username=self.ccid,
                                            password=self.password)

        self.student = Student.objects.create(ccid=self.ccid, first_name=self.first_name,
                                            last_name=self.last_name, email=self.email,
                                            user=self.user, lang_pref=self.lang_pref,
                                            student_id=self.student_id, program = self.program,
                                            year = self.year)

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



    def test_student_apply(self):
        self.award_name = "An Award Name"
        self.award_description = "An Award Description"
        self.award_value = "An Award Value"
        self.award_start_date = date(date.today().year, 1, 1)
        self.award_end_date = date(date.today().year, 12, 31)
        self.award_documents_needed = True
        self.award_is_active = True


        self.award = Award.objects.create(name=self.award_name, description=self.award_description, value=self.award_value,
                                          start_date=self.award_start_date, end_date=self.award_end_date,
                                          documents_needed=self.award_documents_needed, is_active=self.award_is_active)

        self.award.programs.add(self.program)
        self.award.years_of_study.add(self.year)

        award = Award.objects.get(name = self.award_name)


        self.selenium.get('%s%s' % (self.live_server_url, '/awards/'))
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))



        self.selenium.find_element_by_link_text("Apply").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        self.selenium.find_element_by_id("id_application_file").send_keys(settings.TEST_FILE_ROOT+'\selenium_test_apply.pdf')
        self.selenium.find_element_by_name("_save").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))


        application = Application.objects.get(student = self.student, award = self.award)

        self.assertFalse(application.is_submitted)

        self.selenium.find_element_by_link_text("In-Progress Awards").click()
        self.selenium.find_element_by_link_text("Edit").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        self.selenium.find_element_by_name("_delete").click()
        self.selenium.switch_to_alert().accept()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.current_url == ("%s%s" % (self.live_server_url, '/awards/')))


        with self.assertRaises(Application.DoesNotExist):
            application = Application.objects.get(student=self.student, award=self.award)

        self.selenium.find_element_by_link_text("Apply").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        self.selenium.find_element_by_id("id_application_file").send_keys(settings.TEST_FILE_ROOT + '\selenium_test_apply.pdf')
        self.selenium.find_element_by_name("_submit").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        application = Application.objects.get(student=self.student, award=self.award)
        self.assertTrue(application.is_submitted)

        self.selenium.find_element_by_link_text("Submitted Awards").click()
        self.selenium.find_element_by_link_text("Unsubmit").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        application = Application.objects.get(student=self.student, award=self.award)
        self.assertFalse(application.is_submitted)

        self.selenium.find_element_by_link_text("In-Progress Awards").click()
        self.selenium.find_element_by_link_text("Edit").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        self.selenium.find_element_by_id("application_file-clear_id").click()
        self.selenium.find_element_by_name("_save").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        application = Application.objects.get(student=self.student, award=self.award)
        self.assertFalse(application.application_file)



    def test_student_history(self):
        self.award_name = "An Award Name"
        self.award_description = "An Award Description"
        self.award_value = "An Award Value"
        self.award_start_date = datetime.datetime.now(pytz.timezone('America/Vancouver'))
        self.award_end_date = datetime.datetime.now(pytz.timezone('America/Edmonton'))
        self.award_documents_needed = False
        self.award_is_active = True

        self.award = Award.objects.create(name=self.award_name, description=self.award_description,
                                          value=self.award_value,
                                          start_date=self.award_start_date, end_date=self.award_end_date,
                                          documents_needed=self.award_documents_needed, is_active=self.award_is_active)

        self.award.programs.add(self.program)
        self.award.years_of_study.add(self.year)

        self.application = Application.objects.create(student = self.student, award = self.award, is_submitted=True)

        self.selenium.get('%s%s' % (self.live_server_url, '/history/'))
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        src = self.selenium.page_source
        self.assertTrue(self.award_name in src)
        self.assertTrue(self.award_description in src)
        self.assertTrue(self.award_value in src)