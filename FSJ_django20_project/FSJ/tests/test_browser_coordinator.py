from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
#from selenium.webdriver.chrome.webdriver import WebDriver
from ..models import Coordinator
from django.contrib.auth.models import User
import time


class SeleniumTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(SeleniumTest, cls).setUpClass()
        cls.selenium = WebDriver(executable_path=r'C:\Users\Jacqueline\Documents\Cmput 401\geckodriver.exe')
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTest, cls).tearDownClass()



class CoordinatorSeleniumTest(SeleniumTest):
    def setUp(self):
        User.objects.create_superuser(username='admin',
                                      password='admin_password',
                                      email='admin@csjawards.ca')

    def tearDown(self):
        pass

    def test_log_in_admin(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('admin')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('admin_password')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

    def test_create_user(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))
        from selenium.webdriver.support.wait import WebDriverWait
        timeout = 5
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))

        #add_user = self.selenium.find_element_by_css_selector(css_selector="#content-main > div.app-auth.module > table > tbody > tr.model-user > td:nth-child(2) > a")
        #add_user = self.selenium.find_element_by_xpath("//*[@id='content-main']/div[1]/table/tbody/tr[2]/td[1]/a")
        #add_user.click()

        ids = self.selenium.find_elements_by_xpath('//*[@id]')
        for ii in ids:
            # print ii.tag_name
            print(ii.get_attribute('id'))  # id name as string

        ids = self.selenium.find_elements_by_xpath('//*[@id="content-main"]/*')
        for ii in ids:
            # print ii.tag_name
            print(ii.__str__())  # id name as string