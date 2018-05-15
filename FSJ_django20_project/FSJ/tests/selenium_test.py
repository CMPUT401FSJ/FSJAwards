from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

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

