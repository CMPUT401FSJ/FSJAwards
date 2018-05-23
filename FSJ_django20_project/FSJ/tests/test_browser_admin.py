from ..models import *
from django.contrib.auth.models import User
from selenium.webdriver.support.wait import WebDriverWait
timeout = 15
import time
from .selenium_test import SeleniumTest


class AdminSeleniumTest(SeleniumTest):

    @classmethod
    def setUpClass(cls):

        super(AdminSeleniumTest, cls).setUpClass()
        User.objects.create_superuser(username='admin',
                                      password='admin_password',
                                      email='admin@csjawards.ca')

        cls.selenium.get('%s%s' % (cls.live_server_url, '/admin/'))
        username_input = cls.selenium.find_element_by_name("username")
        username_input.send_keys('admin')
        password_input = cls.selenium.find_element_by_name("password")
        password_input.send_keys('admin_password')
        cls.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

    @classmethod
    def tearDownClass(cls):
        super(AdminSeleniumTest, cls).tearDownClass()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_coordinator(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/auth/user/add/'))
        user_name = self.selenium.find_element_by_id("id_username")
        user_name.send_keys("coordinator")
        password_1 = self.selenium.find_element_by_id("id_password1")
        password_1.send_keys("coord_password")
        password_2 = self.selenium.find_element_by_id("id_password2")
        password_2.send_keys("coord_password")

        submit = self.selenium.find_element_by_name("_save")
        submit.click()


        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))

        self.user = User.objects.get(username = "coordinator")
        self.assertEquals(self.user.check_password("coord_password"), True)

        self.selenium.get("%s%s" % (self.live_server_url, '/admin/FSJ/coordinator/add/'))

        self.selenium.find_element_by_css_selector("#id_user > option:nth-child(3)").click()

        self.selenium.find_element_by_id("id_ccid").send_keys("coordinator")
        self.selenium.find_element_by_id("id_first_name").send_keys("A")
        self.selenium.find_element_by_id("id_last_name").send_keys("Coordinator")
        self.selenium.find_element_by_id("id_email").send_keys("coordinator@csjawards.ca")
        self.selenium.find_element_by_name("_save").click()


        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))

        self.selenium.get("%s%s" % (self.live_server_url, '/admin/'))

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))


        self.coordinator = Coordinator.objects.get(ccid="coordinator")
        self.user = User.objects.get(username="coordinator")

        self.assertEquals(self.coordinator.first_name, "A")
        self.assertEquals(self.coordinator.last_name, "Coordinator")
        self.assertEquals(self.coordinator.email, "coordinator@csjawards.ca")
        self.assertEquals(self.coordinator.user, self.user)
        self.assertEquals(self.coordinator.email, self.user.email)
        self.assertEquals(self.coordinator.ccid, self.user.username)


