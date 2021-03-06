from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestProfileChrome(StaticLiveServerTestCase):
    """Testing Profile app interaction with Chrome"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = Chrome()
        cls.selenium.implicitly_wait(5)

        cls.new_user = {
            'email': 'whatever@gmail.net',
            'password': 'Aaaa2468',
            'username': 'johnny',
            'first_name': 'john',
            'last_name': 'Doe',
        }
        cls.user_profile = {
            'profile_phone_number': '+123456789',
            'profile_street_address1': 'Street Address 1',
            'profile_street_address2': 'Street Address 2',
            'profile_postcode': 'P123',
            'profile_town_or_city': 'Town or City',
            'profile_country': 'Country',
        }

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def _signin(self):
        """Navbar dropdown signin should redirect to sign in page"""

        self.selenium.find_element_by_link_text('Account').click()
        self.selenium.find_element_by_link_text('Sign In').click()
        self.assertEqual(self.selenium.current_url,
                         f'{self.live_server_url}/accounts/login/')

        self.selenium.find_element_by_id('id_login').send_keys(
            self.new_user['email'])
        self.selenium.find_element_by_id('id_password').send_keys(
            self.new_user['password'])
        self.selenium.find_element_by_xpath(
            "//form[@action='/accounts/login/']//button[@type='submit']"
        ).click()

    def _signup(self):
        """
        Navbar dropdown signup should redirect to sign up page.
        Successful registration should redirect to home page
        """

        self.selenium.find_element_by_link_text('Account').click()
        self.selenium.find_element_by_link_text('Sign Up').click()
        self.assertEqual(self.selenium.current_url,
                         f'{self.live_server_url}/accounts/signup/')

        self.selenium.find_element_by_id('id_email').send_keys(
            self.new_user['email'])
        self.selenium.find_element_by_id('id_email2').send_keys(
            self.new_user['email'])
        self.selenium.find_element_by_id('id_username').send_keys(
            self.new_user['username'])
        self.selenium.find_element_by_id('id_first_name').send_keys(
            self.new_user['first_name'])
        self.selenium.find_element_by_id('id_last_name').send_keys(
            self.new_user['last_name'])
        self.selenium.find_element_by_id('id_password1').send_keys(
            self.new_user['password'])
        self.selenium.find_element_by_id('id_password2').send_keys(
            self.new_user['password'])
        self.selenium.find_element_by_xpath(
            "//form[@id='signup_form']//button[@type='submit']").click()
        WebDriverWait(self.selenium, 10).until(EC.url_changes)
        self.assertEqual(self.selenium.current_url,
                         f'{self.live_server_url}/')

    def _to_profile(self):
        """
        Authenticated users should access My Profile page from navbar dropdown
        """

        self.selenium.find_element_by_link_text('My Account').click()
        self.selenium.find_element_by_link_text('My Profile').click()
        self.assertEqual(self.selenium.current_url,
                         f'{self.live_server_url}/profile/')

    def _logout(self):
        """
        Autheticated users can logout from the MyAccount navbar dropdown
        """

        self.selenium.find_element_by_link_text('My Account').click()
        self.selenium.find_element_by_link_text('Sign Out').click()
        WebDriverWait(self.selenium, 10).until(EC.url_changes)
        self.assertEqual(self.selenium.current_url,
                         f'{self.live_server_url}/accounts/logout/')
        self.selenium.find_element_by_xpath(
            "//form[@action='/accounts/logout/']//button[@type='submit']"
        ).click()
        WebDriverWait(self.selenium, 10).until(EC.url_changes)
        self.assertEqual(self.selenium.current_url,
                         f'{self.live_server_url}/')

    def test_authentication(self):
        """
        Test grouping registration, My Profile access, logout and
        login process.
        """

        self.selenium.get(f'{self.live_server_url}/')

        self._signup()

        self._to_profile()

        self._logout()

        self._signin()

    def test_password_reset(self):
        """
        Testing password reset
        User should be sent an email (redirected to confirmation page)
        Url link to setnew password not tested yet
        """

        self.selenium.get(f'{self.live_server_url}/')

        self._signup()
        self._logout()

        self.selenium.get(f'{self.live_server_url}/accounts/login/')
        WebDriverWait(self.selenium, 10).until(EC.url_changes)
        self.selenium.find_element_by_link_text('Forgot Password?').click()
        self.assertEqual(self.selenium.current_url,
                         f'{self.live_server_url}/accounts/password/reset/')
        self.selenium.find_element_by_id('id_email')\
            .send_keys(self.new_user['email'])
        self.selenium.find_element_by_xpath(
            '//input[@value="Reset My Password"]').click()
        self.assertEqual(
            self.selenium.current_url,
            f'{self.live_server_url}/accounts/password/reset/done/')

    def test_password_change(self):
        """
        Testing a user changing his password
        Successful change should redirect user to his profile page
        """

        self.selenium.get(f'{self.live_server_url}/')

        self._signup()
        self._to_profile()

        self.selenium.find_element_by_link_text('change password ?').click()
        WebDriverWait(self.selenium, 10).until(EC.url_changes)

        # I'm overriding Allauth PasswordChangeView to change success_url
        # See profile/urls.py
        self.assertEqual(self.selenium.current_url,
                         f'{self.live_server_url}/profile/password-change/')

        self.selenium.find_element_by_id('id_oldpassword').send_keys(
            self.new_user['password'])
        self.selenium.find_element_by_id('id_password1').send_keys(
            'Newpass456')
        self.selenium.find_element_by_id('id_password2').send_keys(
            'Newpass456')
        self.selenium.find_element_by_xpath(
            '//button[text()="Change Password"]').click()
        WebDriverWait(self.selenium, 10).until(EC.url_changes)
        self.assertEqual(self.selenium.current_url,
                         f'{self.live_server_url}/profile/')

    def test_user_updates_profile(self):
        """
        Testing a user updating his profile
        Successful change should redirect user to his profile page with updated
        form fields
        """

        self.selenium.get(f'{self.live_server_url}/')

        self._signup()
        self._to_profile()

        for data in self.user_profile:
            self.selenium.find_element_by_xpath(f'//input[@name="{data}"]')\
                .send_keys(self.user_profile[data])

        self.selenium.find_element_by_xpath(
            '//button[text()="Update Details"]').click()
        WebDriverWait(self.selenium, 10).until(EC.url_changes)
        self.assertEqual(self.selenium.current_url,
                         f'{self.live_server_url}/profile/')

        for data in self.user_profile:
            self.assertEqual(
                self.selenium.find_element_by_xpath(
                    f'//input[@name="{data}"]').get_attribute(
                    'value'),
                self.user_profile[data]
            )

    def test_user_deletes_account(self):
        """
        User deleting his account should be logged out and unable to
        reset a password with old password
        Error Message should be displayed
        """

        self.selenium.get(f'{self.live_server_url}/')
        self._signup()
        self._to_profile()

        self.selenium.find_element_by_link_text('Delete').click()
        self.modal = self.selenium.find_element_by_class_name('modal-dialog')
        self.selenium.find_element_by_link_text('Delete account').click()

        self.assertEqual(self.selenium.current_url,
                         f'{self.live_server_url}/')

        self.selenium.find_element_by_link_text('Account').click()
        self.selenium.find_element_by_link_text('Sign In').click()
        WebDriverWait(self.selenium, 10).until(EC.url_changes)
        self.selenium.find_element_by_link_text('Forgot Password?').click()
        self.selenium.find_element_by_id('id_email') \
            .send_keys(self.new_user['email'])
        self.selenium.find_element_by_xpath(
            '//input[@value="Reset My Password"]').click()
        self.assertEqual(
            self.selenium.find_element_by_class_name('form-field-error').text,
            '* The e-mail address is not assigned to any user account'
        )
