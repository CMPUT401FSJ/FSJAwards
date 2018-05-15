from ..models import *
from django.contrib.auth.models import User
from selenium.webdriver.support.wait import WebDriverWait
timeout = 15
import time
from .selenium_test import SeleniumTest

class CoordinatorSeleniumTest(SeleniumTest):

    @classmethod
    def setUpClass(cls):
        super(CoordinatorSeleniumTest, cls).setUpClass()
        cls.password = "coord_password"
        cls.ccid = "coordinator"
        cls.first_name = "A"
        cls.last_name = "Coordinator"
        cls.email = "coordinator@csjawards.ca"


        cls.user = User.objects.create_user(username=cls.ccid,
                                      password=cls.password)


        cls.coordinator = Coordinator.objects.create(ccid=cls.ccid, first_name=cls.first_name,
                                   last_name=cls.last_name, email=cls.email,
                                   user = cls.user)

        cls.user = User.objects.get(username = cls.ccid)



    def setUp(self):

        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username = self.selenium.find_element_by_id("id_username")
        username.send_keys(self.ccid)
        password =self.selenium.find_element_by_id("id_password")
        password.send_keys(self.password)

        save = self.selenium.find_element_by_css_selector("button.btn:nth-child(5)")
        save.click()

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))

    def tearDown(self):
        pass

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

        # WebDriverWait(self.selenium, timeout).until(
        #     lambda driver: driver.find_element_by_tag_name('body'))
        #
        # self.assertEquals(self.selenium.current_url, ("%s%s" % (self.live_server_url, '/awards/')))
        #
        # self.selenium.get('%s%s' % (self.live_server_url, '/awards/'))

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

        self.award_program.delete()
        self.award_year.delete()




    # def test_coordinator_cancel_award(self):
    #
    #     self.selenium.get('%s%s' % (self.live_server_url, '/awards/add/'))
    #
    #     WebDriverWait(self.selenium, timeout).until(
    #         lambda driver: driver.find_element_by_tag_name('body'))
    #
    #     self.selenium.find_element_by_id("id_name").send_keys(self.award_name)
    #     self.selenium.find_element_by_id("id_description").send_keys(self.award_description)
    #     self.selenium.find_element_by_id("id_value").send_keys(self.award_value)
    #     self.selenium.find_element_by_css_selector("#id_programs_0").click()
    #     self.selenium.find_element_by_css_selector("#id_years_of_study_0").click()
    #     self.selenium.find_element_by_id("id_start_date").send_keys(self.start_date)
    #     self.selenium.find_element_by_id("id_end_date").send_keys(self.end_date)
    #     self.selenium.find_element_by_id("id_documents_needed").click()
    #     self.selenium.find_element_by_id("id_is_active").click()
    #     self.selenium.find_element_by_css_selector("a.btn.btn-danger").click()
    #
    #     WebDriverWait(self.selenium, timeout).until(
    #         lambda driver: driver.find_element_by_tag_name('body'))
    #
    #     self.assertEquals(self.selenium.current_url, ("%s%s" % (self.live_server_url, '/awards/')))
    #
    #     with self.assertRaises(Award.DoesNotExist):
    #         award = Award.objects.get(name=self.award_name)