from ..models import *
from django.contrib.auth.models import User
from selenium.webdriver.support.wait import WebDriverWait
timeout = 15
import time
import pytz
import datetime
from .selenium_test import SeleniumTest
from django.conf import settings
from selenium.webdriver.firefox.webdriver import WebDriver


class CoordinatorSeleniumTest(SeleniumTest):

    @classmethod
    def setUpClass(cls):
        super(CoordinatorSeleniumTest, cls).setUpClass()


    def setUp(self):
        self.password = "coord_password"
        self.ccid = "coordinator"
        self.first_name = "A"
        self.last_name = "Coordinator"
        self.email = "coordinator@csjawards.ca"
        self.lang_pref = "en"

        self.user = User.objects.create_user(username=self.ccid,
                                            password=self.password)

        self.coordinator = Coordinator.objects.create(ccid=self.ccid, first_name=self.first_name,
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

    def test_coordinator_awards(self):
        self.award_name = "An Award Name"
        self.award_description = "An Award Description"
        self.new_award_description = "This is a new description"
        self.award_value = "An Award Value"
        self.program_name = "A Program Name"
        self.program_code = "A Code"
        self.year_name = "Year 1"
        self.award_program = Program.objects.create(name=self.program_name, code=self.program_code)
        self.award_year = YearOfStudy.objects.create(year=self.year_name)
        self.start_date = "2018-01-01"
        self.end_date = "2018-12-31"
        self.new_start_date = "2019-01-01"
        self.new_end_date = "2019-12-31"

        self.selenium.get('%s%s' % (self.live_server_url, '/awards/'))
        self.selenium.find_element_by_link_text("Add award").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))

        self.assertEquals(self.selenium.current_url, ("%s%s" % (self.live_server_url, '/awards/add/')))


        self.selenium.find_element_by_id("id_name").send_keys(self.award_name)
        self.selenium.find_element_by_id("id_description").send_keys(self.award_description)
        self.selenium.find_element_by_id("id_value").send_keys(self.award_value)
        self.selenium.find_element_by_css_selector("#id_programs_0").click()
        self.selenium.find_element_by_css_selector("#id_years_of_study_0").click()
        self.selenium.find_element_by_id("id_start_date").send_keys(self.start_date)
        self.selenium.find_element_by_id("id_end_date").send_keys(self.end_date)
        self.selenium.find_element_by_id("id_documents_needed").click()
        self.selenium.find_element_by_id("id_is_active").click()
        self.selenium.find_element_by_css_selector("button.btn.btn-success").click()


        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.current_url == ("%s%s" % (self.live_server_url, '/awards/')))


        award = Award.objects.get(name = self.award_name)
        self.assertEquals(award.description, self.award_description)
        self.assertEquals(award.value, self.award_value)
        self.assertEquals(award.programs.get(code=self.program_code), self.award_program)
        self.assertEquals(award.years_of_study.get(year=self.year_name), self.award_year)
        self.assertEquals(award.start_date.strftime('%Y-%m-%d'), self.start_date)
        self.assertEquals(award.end_date.strftime('%Y-%m-%d'), self.end_date)
        self.assertEquals(award.documents_needed, True)
        self.assertEquals(award.is_active, True)

        WebDriverWait(self.selenium, timeout).until(
                 lambda driver: driver.find_element_by_name("awardaction"))


        self.selenium.find_element_by_name("awardaction").click()
        self.selenium.find_element_by_name("_deactivate").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_name("awardaction"))

        award.refresh_from_db()
        self.assertEquals(award.is_active, False)

        self.selenium.find_element_by_name("awardaction").click()
        self.selenium.find_element_by_name("_activate").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_name("awardaction"))

        award.refresh_from_db()
        self.assertEquals(award.is_active, True)

        self.selenium.find_element_by_name("awardaction").click()
        self.selenium.find_element_by_css_selector("div.div-restrict-width:nth-child(13) > div:nth-child(2) > input:nth-child(1)").send_keys(self.new_start_date)
        self.selenium.find_element_by_css_selector("div.div-restrict-width:nth-child(14) > div:nth-child(2) > input:nth-child(1)").send_keys(self.new_end_date)
        self.selenium.find_element_by_name("_changeDate").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_name("awardaction"))

        award.refresh_from_db()
        self.assertEquals(award.start_date.strftime('%Y-%m-%d'), self.new_start_date)
        self.assertEquals(award.end_date.strftime('%Y-%m-%d'), self.new_end_date)

        self.selenium.find_element_by_link_text("Edit").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id("id_description"))

        description = self.selenium.find_element_by_id("id_description")
        description.clear()
        description.send_keys(self.new_award_description)
        self.selenium.find_element_by_css_selector("button.btn.btn-success").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_name("awardaction"))

        award.refresh_from_db()
        self.assertEquals(award.description, self.new_award_description)


        self.selenium.find_element_by_name("awardaction").click()
        self.selenium.find_element_by_css_selector("button.btn.btn-danger.pull-right").click()
        self.selenium.switch_to_alert().accept()


        time.sleep(5)

        with self.assertRaises(Award.DoesNotExist):
            award = Award.objects.get(name=self.award_name)

        self.selenium.find_element_by_link_text("Add award").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))

        self.assertEquals(self.selenium.current_url, ("%s%s" % (self.live_server_url, '/awards/add/')))

        self.selenium.find_element_by_id("id_name").send_keys(self.award_name)
        self.selenium.find_element_by_id("id_description").send_keys(self.award_description)
        self.selenium.find_element_by_id("id_value").send_keys(self.award_value)
        self.selenium.find_element_by_css_selector("#id_programs_0").click()
        self.selenium.find_element_by_css_selector("#id_years_of_study_0").click()
        self.selenium.find_element_by_id("id_start_date").send_keys(self.start_date)
        self.selenium.find_element_by_id("id_end_date").send_keys(self.end_date)
        self.selenium.find_element_by_id("id_documents_needed").click()
        self.selenium.find_element_by_id("id_is_active").click()
        self.selenium.find_element_by_link_text("Cancel").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))

        with self.assertRaises(Award.DoesNotExist):
            award = Award.objects.get(name=self.award_name)



    def test_coordinator_students(self):

        self.student_ccid = "student"
        self.student_first_name = "A"
        self.student_middle_name = "Normal"
        self.student_last_name = "Student"
        self.student_ualberta_id = "123456789"
        self.program_name = "A Program Name"
        self.program_code = "A Code"
        self.year_name = "Year 1"
        self.student_program = Program.objects.create(name=self.program_name, code=self.program_code)
        self.student_year = YearOfStudy.objects.create(year=self.year_name)
        self.student_email = "student@csjawards.ca"
        self.student_gpa = "4.0"

        self.new_student_first_name = "New"
        self.new_student_middle_name = "Student"
        self.new_student_last_name = "Name"


        self.selenium.get('%s%s' % (self.live_server_url, '/students/'))
        self.selenium.find_element_by_link_text("Add student").click()

        self.selenium.find_element_by_id("id_ccid").send_keys(self.student_ccid)
        self.selenium.find_element_by_id("id_first_name").send_keys(self.student_first_name)
        self.selenium.find_element_by_id("id_middle_name").send_keys(self.student_middle_name)
        self.selenium.find_element_by_id("id_last_name").send_keys(self.student_last_name)
        self.selenium.find_element_by_id("id_email").send_keys(self.student_email)
        self.selenium.find_element_by_css_selector("#id_program > option:nth-child(2)").click()
        self.selenium.find_element_by_css_selector("#id_year > option:nth-child(2)").click()
        self.selenium.find_element_by_id("id_student_id").send_keys(self.student_ualberta_id)
        self.selenium.find_element_by_id("id_gpa").send_keys(self.student_gpa)
        self.selenium.find_element_by_css_selector("button.btn.btn-success").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_name("instance"))


        student = Student.objects.get(ccid = self.student_ccid)
        self.assertEquals(student.first_name, self.student_first_name)
        self.assertEquals(student.middle_name, self.student_middle_name)
        self.assertEquals(student.last_name, self.student_last_name)
        self.assertEquals(student.email, self.student_email)
        self.assertEquals(student.program, self.student_program)
        self.assertEquals(student.year, self.student_year)
        self.assertEquals(student.student_id, self.student_ualberta_id)
        self.assertEquals(student.gpa, self.student_gpa)

        user = User.objects.get(username = self.student_ccid)
        self.assertEquals(student.user, user)
        self.assertEquals(student.email, user.email, self.student_email)


        self.selenium.find_element_by_link_text("Edit").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id("id_first_name"))

        first_name = self.selenium.find_element_by_id("id_first_name")
        first_name.clear()
        first_name.send_keys(self.new_student_first_name)
        middle_name = self.selenium.find_element_by_id("id_middle_name")
        middle_name.clear()
        middle_name.send_keys(self.new_student_middle_name)
        last_name = self.selenium.find_element_by_id("id_last_name")
        last_name.clear()
        last_name.send_keys(self.new_student_last_name)
        self.selenium.find_element_by_css_selector("button.btn.btn-success").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_name("instance"))


        student.refresh_from_db()
        self.assertEquals(student.first_name, self.new_student_first_name)
        self.assertEquals(student.middle_name, self.new_student_middle_name)
        self.assertEquals(student.last_name, self.new_student_last_name)

        self.selenium.find_element_by_name("instance").click()
        self.selenium.find_element_by_name("delete").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_link_text("Upload files"))

        with self.assertRaises(Student.DoesNotExist):
            student = Student.objects.get(ccid = self.student_ccid)

        with self.assertRaises(User.DoesNotExist):
            user = User.objects.get(username = self.student_ccid)


        self.selenium.find_element_by_link_text("Upload files").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id("id_student_file"))

        self.selenium.find_element_by_id("id_student_file").send_keys(settings.TEST_FILE_ROOT+'\selenium_test_student.csv')
        self.selenium.find_element_by_id("id_gpa_file").send_keys(settings.TEST_FILE_ROOT+'\selenium_test_gpa.csv')
        self.selenium.find_element_by_css_selector("button.btn.btn-success").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        self.selenium.get('%s%s' % (self.live_server_url, '/students/'))

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        student = Student.objects.get(ccid=self.student_ccid)
        self.assertEquals(student.first_name, self.student_first_name)
        self.assertEquals(student.middle_name, self.student_middle_name)
        self.assertEquals(student.last_name, self.student_last_name)
        self.assertEquals(student.email, self.student_email)
        self.assertEquals(student.program, self.student_program)
        self.assertEquals(student.year, self.student_year)
        self.assertEquals(student.student_id, self.student_ualberta_id)
        self.assertEquals(student.gpa, self.student_gpa)



    def test_coordinator_adjudicators(self):

        self.adjudicator_ccid = "adjudicator"
        self.adjudicator_first_name = "An"
        self.adjudicator_last_name = "Adjudicator"
        self.adjudicator_email = "adjudicator@csjawards.ca"

        self.new_adjudicator_email = "newadjudicatoremail@csjawards.ca"

        self.selenium.get('%s%s' % (self.live_server_url, '/adjudicators/'))

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        self.selenium.find_element_by_link_text("Add adjudicator").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        self.selenium.find_element_by_id("id_ccid").send_keys(self.adjudicator_ccid)
        self.selenium.find_element_by_id("id_first_name").send_keys(self.adjudicator_first_name)
        self.selenium.find_element_by_id("id_last_name").send_keys(self.adjudicator_last_name)
        self.selenium.find_element_by_id("id_email").send_keys(self.adjudicator_email)
        self.selenium.find_element_by_css_selector("button.btn.btn-success").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.current_url == ("%s%s" % (self.live_server_url, '/adjudicators/')))


        adjudicator = Adjudicator.objects.get(ccid=self.adjudicator_ccid)
        self.assertEquals(adjudicator.first_name, self.adjudicator_first_name)
        self.assertEquals(adjudicator.last_name, self.adjudicator_last_name)
        self.assertEquals(adjudicator.email, self.adjudicator_email)

        user = User.objects.get(username=self.adjudicator_ccid)
        self.assertEquals(adjudicator.user, user)
        self.assertEquals(adjudicator.user.email, user.email, self.adjudicator_email)

        self.selenium.find_element_by_link_text("Edit").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        email = self.selenium.find_element_by_id("id_email")
        email.clear()
        email.send_keys(self.new_adjudicator_email)
        self.selenium.find_element_by_css_selector("button.btn.btn-success").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        adjudicator.refresh_from_db()
        user.refresh_from_db()

        self.assertEquals(adjudicator.email, user.email, self.new_adjudicator_email)

        self.selenium.find_element_by_name("instance").click()
        self.selenium.find_element_by_css_selector("button.btn.btn-danger").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        with self.assertRaises(Adjudicator.DoesNotExist):
            adjudicator = Adjudicator.objects.get(ccid = self.adjudicator_ccid)

        with self.assertRaises(User.DoesNotExist):
            user = User.objects.get(username = self.adjudicator_ccid)


    def test_coordinator_committees(self):
        self.committee_name = "A Committee"
        self.adjudicator_ccid = "adjudicator"
        self.adjudicator_first_name = "An"
        self.adjudicator_last_name = "Adjudicator"
        self.adjudicator_email = "adjudicator@csjawards.ca"
        self.adjudicator = Adjudicator.objects.create(ccid = self.adjudicator_ccid, first_name = self.adjudicator_first_name,
                                                      last_name = self.adjudicator_last_name, email = self.adjudicator_email)

        self.year = "First"
        self.year_of_study = YearOfStudy.objects.create(year=self.year)
        self.program_code = "PRFG"
        self.program_name = "Science"
        self.program = Program.objects.create(code=self.program_code, name=self.program_name)

        self.award_name = "This award"
        self.award_description = "For students"
        self.award_value = "One gold pen"
        self.award_start_date = str(datetime.datetime.now(pytz.timezone('America/Vancouver')))
        self.award_end_date = str(datetime.datetime.now(pytz.timezone('America/Edmonton')))
        self.award_documents_needed = False
        self.award_is_active = True
        self.award = Award.objects.create(name=self.award_name, description=self.award_description, value=self.award_value,
                                          start_date=self.award_start_date, end_date=self.award_end_date,
                                          documents_needed=self.award_documents_needed, is_active=self.award_is_active)
        self.award.programs.add(self.program)
        self.award.years_of_study.add(self.year_of_study)



        self.selenium.get('%s%s' % (self.live_server_url, '/committees/'))

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        self.selenium.find_element_by_link_text("Add Committee").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        self.selenium.find_element_by_id("id_committee_name").send_keys(self.committee_name)
        self.selenium.find_element_by_id("id_adjudicators_0").click()
        self.selenium.find_element_by_id("id_awards_0").click()
        self.selenium.find_element_by_css_selector("button.btn.btn-success").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        committee = Committee.objects.get(committee_name = self.committee_name)
        self.assertEquals(committee.adjudicators.get(ccid = self.adjudicator_ccid), self.adjudicator)
        self.assertEquals(committee.awards.get(name = self.award_name), self.award)

        self.second_award_name = "A different award"
        self.second_award = Award.objects.create(name=self.second_award_name, description=self.award_description,
                                                 value=self.award_value,
                                                 start_date=self.award_start_date, end_date=self.award_end_date,
                                                 documents_needed=self.award_documents_needed,
                                                 is_active=self.award_is_active)

        self.selenium.find_element_by_link_text("Edit").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        self.selenium.find_element_by_id("id_awards_1").click()
        self.selenium.find_element_by_css_selector("button.btn.btn-success").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        committee.refresh_from_db()
        self.assertEquals(committee.awards.get(name = self.second_award_name), self.second_award)


        self.selenium.find_element_by_name("instance").click()
        self.selenium.find_element_by_name("delete").click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name("body"))

        with self.assertRaises(Committee.DoesNotExist):
            committee = Committee.objects.get(committee_name = self.committee_name)


