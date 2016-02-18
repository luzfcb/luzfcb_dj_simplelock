import datetime

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from pyvirtualdisplay import Display
from splinter.browser import Browser


class SplinterStaticLiveServerTestCase(StaticLiveServerTestCase):
    # fixtures = ['user-data.json']
    splinter_driver = 'firefox'
    virtual_display_size = (1024, 768)
    use_virtual_display = True

    @classmethod
    def setUpClass(cls):
        super(SplinterStaticLiveServerTestCase, cls).setUpClass()
        if cls.use_virtual_display:
            cls.virtual_display = Display(visible=0, size=cls.virtual_display_size)
            cls.virtual_display.start()
        cls.browser = Browser(cls.splinter_driver)
        cls.browser.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        super(SplinterStaticLiveServerTestCase, cls).tearDownClass()
        cls.browser.quit()
        if cls.use_virtual_display:
            cls.virtual_display.stop()

    def open(self, url):
        self.browser.visit("%s%s" % (self.live_server_url, url))

    def wait_for_seconds(self, time_out_in_seconds):
        current_time = datetime.datetime.now()
        end_time = current_time + datetime.timedelta(seconds=time_out_in_seconds)

        while current_time < end_time:
            current_time = datetime.datetime.now()

    def wait_for_milliseconds(self, time_out_in_milliseconds):
        current_time = datetime.datetime.now()
        end_time = current_time + datetime.timedelta(milliseconds=time_out_in_milliseconds)

        while current_time < end_time:
            current_time = datetime.datetime.now()

    def login_as(self, username, password):

        self.browser.visit(self.live_server_url + '/admin/logout/')
        username_field = self.browser.find_by_css('form input[name="username"]')
        password_field = self.browser.find_by_css('form input[name="password"]')
        username_field.fill(username)
        password_field.fill(password)

        submit = self.browser.find_by_css('form input[type="submit"]')
        submit.click()
        self.wait_for_milliseconds(100)
        print("terminado login")
