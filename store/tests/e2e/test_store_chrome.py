"""
A product is required to be created with an image,
More details in store's 'test_models.py'

Ideally fixtures should be added to run tests with reasonable number of
real products so to better test the interaction, layout and elements on page
I'll take care of that later
"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from store.models import Product, new_image_path, Category
from django.core.files.images import ImageFile
from django.conf import settings
import shutil


class TestStoreChrome(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = Chrome()
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        """
        Create a product with its required fields and media files before
        each tests
        """

        self.django_cat = Category.objects.create(name='django')
        self.product_data = {
            'name': 'test product name',
            'description': 'test product description',
            'base_price': 49.99,
        }
        with open(f'{settings.BASE_DIR}/store/tests/_test_file_1.png',
                  'rb') as image_file:
            image = ImageFile(image_file)

            self.product = Product(**self.product_data)
            self.product.image.save(
                new_image_path(self.product, image.name), image)
            self.product.category = self.django_cat
            self.product.save()

    def tearDown(self):
        """
        Remove product's media file in directory after tests,
        test database is automatically cleared
        """

        # Comment out to check path & file creation
        product_path = f'media/products/{self.product.sku}'
        shutil.rmtree(product_path)

    def test_nav_to_store(self):
        """Test navigation to the store's product via the side bar nav"""

        self.selenium.get(f'{self.live_server_url}/')
        WebDriverWait(self.selenium, 10).until(ec.url_changes)
        self.selenium.find_element_by_class_name("slide-in-btn").click()
        self.selenium.find_element_by_link_text("Everything").click()
        WebDriverWait(self.selenium, 10).until(ec.url_changes)
        self.assertEqual(self.selenium.current_url,
                         f'{self.live_server_url}/store/')

    def test_query_specific_category(self):
        """Should render the store page with a specific category"""

        self.selenium.get(f'{self.live_server_url}/')
        WebDriverWait(self.selenium, 10).until(ec.url_changes)
        self.selenium.find_element_by_class_name("slide-in-btn").click()
        self.selenium.find_element_by_link_text("Marvel").click()
        WebDriverWait(self.selenium, 10).until(ec.url_changes)
        self.assertEqual(self.selenium.current_url,
                         f'{self.live_server_url}/store/?category=marvel')

    def test_query_multiple_categories(self):
        """Should render the store page with multiple selected categories"""

        self.selenium.get(f'{self.live_server_url}/')
        WebDriverWait(self.selenium, 10).until(ec.url_changes)
        self.selenium.find_element_by_class_name("slide-in-btn").click()
        self.selenium.find_element_by_link_text("Home & Garden").click()
        WebDriverWait(self.selenium, 10).until(ec.url_changes)
        self.assertEqual(self.selenium.current_url,
                         f'{self.live_server_url}/store/?category=home,garden')

    def test_nav_to_a_product_detail_page(self):
        """
        Product(s) should be rendered as cards in store template containing
        image and text links to the product_details template
        """

        self.selenium.get(f'{self.live_server_url}/')
        self.selenium.get(f'{self.live_server_url}/store/')
        WebDriverWait(self.selenium, 10).until(ec.url_changes)

        # Store product(s) should be rendered as an article with 2 links
        # containing its product id
        product_img_link = self.selenium.find_element_by_xpath(
            "//article//a")
        self.assertEqual(
            product_img_link.get_attribute('href'),
            f'{self.live_server_url}/store/{self.product.id}/')

        product_txt_link = self.selenium.find_element_by_xpath(
            "//article//h5//a")
        self.assertEqual(
            product_txt_link.get_attribute('href'),
            f'{self.live_server_url}/store/{self.product.id}/')

        self.selenium.find_element_by_class_name(
            "store-card-img").click()
        self.assertEqual(self.selenium.current_url,
                         f'{self.live_server_url}/store/{self.product.id}/')

    def test_search_toolbar(self):
        """
        Using search toolbar should return store template with product(s)
        containing the keyword(s)
        Test is run twice to search for product name and description matching
        """

        keywords = ['product name', 'product description']

        for keyword in keywords:

            self.selenium.get(f'{self.live_server_url}/')

            self.selenium.find_element_by_xpath(
                "//div[@class='search-bar']//input[@name='q']") \
                .send_keys(keyword)
            self.selenium.find_element_by_xpath(
                "//div[@class='search-bar']//button[@type='submit']") \
                .click()

            # Text query search should be in url
            self.assertIn(
                self.selenium.current_url,
                [f'{self.live_server_url}/store/?q=product+name',
                 f'{self.live_server_url}/store/?q=product+description'])

            # Search key word should be in card's name or description
            product_title = self.selenium.find_element_by_xpath(
                "//article//h5//a")
            product_description = self.selenium.find_element_by_xpath(
                "//article//p")
            full_text = ', '.join([product_title.text,
                                   product_description.text])
            self.assertIn(keyword, full_text)

    def test_sort_results_by_price(self):
        """
        Results should be sorted by highest price then lowest first
        Sort bar should be updated
        """

        self.selenium.get(f'{self.live_server_url}/store/')
        self.selenium.find_element_by_id('sort-selector').click()
        self.selenium.find_element_by_xpath(
            '//select[@id="sort-selector"]//option[@value="price_asc"]'
        ).click()
        WebDriverWait(self.selenium, 10).until(ec.url_changes)
        self.assertEqual(
            self.selenium.current_url,
            f'{self.live_server_url}/store/?sort=price&direction=asc')
        bar = self.selenium.find_element_by_xpath(
            '//select[@id="sort-selector"]//option[@selected]')
        self.assertEqual(bar.text.strip(), 'Lowest price')

        self.selenium.find_element_by_id('sort-selector').click()
        self.selenium.find_element_by_xpath(
            '//select[@id="sort-selector"]//option[@value="price_desc"]'
        ).click()
        WebDriverWait(self.selenium, 10).until(ec.url_changes)
        self.assertEqual(
            self.selenium.current_url,
            f'{self.live_server_url}/store/?sort=price&direction=desc')
        bar = self.selenium.find_element_by_xpath(
            '//select[@id="sort-selector"]//option[@selected]')
        self.assertEqual(bar.text.strip(), 'Highest price')

    def test_sort_results_by_date(self):
        """
        Results should be sorted by latest products then oldest
        Sort bar should be updated
        """

        self.selenium.get(f'{self.live_server_url}/store/')
        self.selenium.find_element_by_id('sort-selector').click()
        self.selenium.find_element_by_xpath(
            '//select[@id="sort-selector"]//option[@value="date_desc"]'
        ).click()
        WebDriverWait(self.selenium, 10).until(ec.url_changes)
        self.assertEqual(
            self.selenium.current_url,
            f'{self.live_server_url}/store/?sort=date&direction=desc')
        bar = self.selenium.find_element_by_xpath(
            '//select[@id="sort-selector"]//option[@selected]')
        self.assertEqual(bar.text.strip(), 'Latest')

        self.selenium.find_element_by_id('sort-selector').click()
        self.selenium.find_element_by_xpath(
            '//select[@id="sort-selector"]//option[@value="date_asc"]'
        ).click()
        WebDriverWait(self.selenium, 10).until(ec.url_changes)
        self.assertEqual(
            self.selenium.current_url,
            f'{self.live_server_url}/store/?sort=date&direction=asc')
        bar = self.selenium.find_element_by_xpath(
            '//select[@id="sort-selector"]//option[@selected]')
        self.assertEqual(bar.text.strip(), 'Oldest')

    def test_reset_sort_param(self):
        """
        Should set back the Product sorting to its Model's default
        (latest then name). Requires fixtures to test this further
        """

        self.selenium.get(f'{self.live_server_url}/store/')
        self.selenium.find_element_by_id('sort-selector').click()
        self.selenium.find_element_by_xpath(
            '//select[@id="sort-selector"]//option[@value="reset"]'
        ).click()
        WebDriverWait(self.selenium, 10).until(ec.url_changes)
        self.assertEqual(
            self.selenium.current_url,
            f'{self.live_server_url}/store/')

    def test_search_query_results_feedback(self):
        """
        Search result string (top of results) should contain categories and
        keywords the user has selected
        """

        self.selenium.get(f'{self.live_server_url}/')
        self.selenium.find_element_by_xpath(
            "//div[@class='search-bar']//input[@name='q']") \
            .send_keys('product name')
        self.selenium.find_element_by_xpath(
            "//div[@class='search-bar']//button[@type='submit']") \
            .click()

        search_string = self.selenium.find_element_by_css_selector(
            '.main-wrapper header p')
        self.assertEqual(search_string.text,
                         "1 Product found for ' product name '")

        self.selenium.find_element_by_id(
            "categories-selector").click()
        self.selenium.find_element_by_css_selector(
            "#categories-selection li").click()
        self.selenium.find_element_by_xpath(
            "//div[@class='search-bar']//button[@type='submit']") \
            .click()
        search_string = self.selenium.find_element_by_css_selector(
            '.main-wrapper header p')

        # First letter of category capitalized by template filter
        self.assertEqual(search_string.text,
                         "1 Product found for ' product name ' in Django")

    def test_search_bar_category(self):
        """
        Available categories should be in search bar dropdown to filter search
        results. Categories should remain selected on search results.
        """

        self.selenium.get(f'{self.live_server_url}/')
        self.selenium.find_element_by_id("categories-selector").click()

        categories_selection = self.selenium.find_elements_by_css_selector(
            "#categories-selection li")
        categories = Category.objects.all()
        self.assertEqual(len(categories), len(categories_selection))

        category = self.selenium.find_element_by_css_selector(
            "#categories-selection li")

        category.click()
        self.selenium.find_element_by_id("categories-selector").click()
        self.assertEqual(category.get_attribute('class'),
                         'dropdown-item active-selection')

        self.selenium.find_element_by_xpath(
            "//div[@class='search-bar']//button[@type='submit']") \
            .click()
        WebDriverWait(self.selenium, 10).until(ec.url_changes)

        self.selenium.find_element_by_id("categories-selector").click()
        category = self.selenium.find_element_by_css_selector(
            "#categories-selection li")
        self.assertEqual(category.get_attribute('class'),
                         'dropdown-item active-selection')
