import datetime

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from splinter.browser import Browser


class SplinterStaticLiveServerTestCase(StaticLiveServerTestCase):
    # fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super(SplinterStaticLiveServerTestCase, cls).setUpClass()
        cls.browser = Browser('firefox')

    @classmethod
    def tearDownClass(cls):
        super(SplinterStaticLiveServerTestCase, cls).tearDownClass()
        cls.browser.quit()


    def open(self, url):
        self.browser.visit("%s%s" % (self.live_server_url, url))

    def wait_for_seconds(self, time_out_in_seconds):
        current_time = datetime.datetime.now()
        end_time = current_time + datetime.timedelta(0, time_out_in_seconds)

        while current_time < end_time:
            current_time = datetime.datetime.now()


    def login_as(self, browser, username, password):

        browser.visit(self.live_server_url + '/admin/logout/')
        username_field = browser.find_by_css('form input[name="username"]')
        password_field = browser.find_by_css('form input[name="password"]')
        username_field.fill(username)
        password_field.fill(password)

        submit = browser.find_by_css('form input[type="submit"]')
        submit.click()
