from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from core.models import Metal, Material, Category, Jewelry, Review


class TestWalkPage(StaticLiveServerTestCase):
    def setUp(self):
        self.metal1 = Metal.objects.create(title="met1", slug="met1_slug")
        self.metal2 = Metal.objects.create(title="met2", slug="met2_slug")
        self.material1 = Material.objects.create(title="mat1", slug="mat1_slug")
        self.material2 = Material.objects.create(title="mat2", slug="mat2_slug")
        self.category1 = Category.objects.create(title="cat1", slug="cat1_slug")
        self.category2 = Category.objects.create(title="cat2", slug="cat2_slug")

        self.jew1 = Jewelry.objects.create(
            title="jew1",
            slug="jew1_slug",
            price=100,
            is_in_stock=True,
            jew_cat=self.category1,
            metal_cat=self.metal1,
            main_photo="image.jpg"
        )
        self.jew1.material_cats.add(self.material1)
        self.jew2 = Jewelry.objects.create(
            title="jew2",
            slug="jew2_slug",
            price=200,
            is_in_stock=True,
            jew_cat=self.category1,
            metal_cat=self.metal2,
            main_photo="image.jpg"
        )
        self.jew2.material_cats.add(self.material2)
        self.jew2.material_cats.add(self.material1)
        self.jew3 = Jewelry.objects.create(
            title="jew3",
            slug="jew3_slug",
            price=150,
            is_in_stock=True,
            jew_cat=self.category2,
            metal_cat=self.metal1,
            main_photo="image.jpg"
        )
        self.jew3.material_cats.add(self.material2)
        self.jew4 = Jewelry.objects.create(
            title="jew4",
            slug="jew4_slug",
            price=250,
            is_in_stock=True,
            jew_cat=self.category2,
            metal_cat=self.metal2,
            main_photo="image.jpg"
        )
        self.jew4.material_cats.add(self.material1)
        self.jew4.material_cats.add(self.material2)
        self.jew5 = Jewelry.objects.create(
            title="jew5",
            slug="jew5_slug",
            price=300,
            is_in_stock=False,
            jew_cat=self.category1,
            metal_cat=self.metal1,
            main_photo="image.jpg"
        )
        self.jew5.material_cats.add(self.material1)

        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def tearDown(self):
        self.browser.quit()


class TestHomePage(TestWalkPage):
    def setUp(self):
        self.review1 = Review.objects.create(title="Rev1", stars=5, text="Some text. Some text. Some text. Some text")
        self.review2 = Review.objects.create(title="Rev2", stars=5, text="Some text. Some text. Some text. Some text")
        self.review3 = Review.objects.create(title="Rev3", stars=5, text="Some text. Some text. Some text. Some text")
        self.review4 = Review.objects.create(title="Rev4", stars=5, text="Some text. Some text. Some text. Some text")
        self.review5 = Review.objects.create(title="Rev5", stars=5, text="Some text. Some text. Some text. Some text")
        super().setUp()

    def test_reviews(self):
        self.browser.get(self.live_server_url)
        btn_next = self.browser.find_element(By.CSS_SELECTOR, "button.carousel-control-next")
        btn_prev = self.browser.find_element(By.CSS_SELECTOR, "button.carousel-control-prev")
        btn_next.click()
        btn_prev.click()

    def test_news(self):
        self.browser.get(self.live_server_url)
        news = self.browser.find_elements(By.CSS_SELECTOR, "#news .card-item")
        self.assertEqual(len(news), 3)
        links = [new.find_element(By.TAG_NAME, 'a').get_attribute("href") for new in news]
        for link in links:
            self.browser.get(link)


class TestUser(TestWalkPage):
    hard_password = "My123The456Password"
    light_password = "12345"
    right_email = "testing@test.com"
    wrong_email = "test.com"

    def test_success_registration(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.CSS_SELECTOR, "#menu li:nth-child(7) a").click()

        name_field = self.browser.find_element(By.NAME, "username")
        name_field.send_keys("Тестер")
        email_field = self.browser.find_element(By.NAME, "email")
        email_field.send_keys(self.right_email)
        password1_filed = self.browser.find_element(By.NAME, "password1")
        password1_filed.send_keys(self.hard_password)
        password2_filed = self.browser.find_element(By.NAME, "password2")
        password2_filed.send_keys(self.hard_password)
        submit_btn = self.browser.find_element(By.TAG_NAME, "button")
        submit_btn.click()

        self.browser.find_element(By.CSS_SELECTOR, "#my_cart").click()
        cart = self.browser.find_element(By.CSS_SELECTOR, "#cart p").text
        self.assertEqual(cart, "Пока товаров нет")

    def test_fail_registration(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.CSS_SELECTOR, "#menu li:nth-child(7) a").click()

        name_field = self.browser.find_element(By.NAME, "username")
        name_field.send_keys("Тестер")
        email_field = self.browser.find_element(By.NAME, "email")
        email_field.send_keys(self.wrong_email)
        password1_filed = self.browser.find_element(By.NAME, "password1")
        password1_filed.send_keys(self.light_password)
        password2_filed = self.browser.find_element(By.NAME, "password2")
        password2_filed.send_keys(self.light_password)
        submit_btn = self.browser.find_element(By.TAG_NAME, "button")
        submit_btn.click()

        with self.assertRaises(NoSuchElementException):
            self.browser.find_element(By.CSS_SELECTOR, "#menu li:nth-child(6) ul li:nth-child(3) a").click()


class TestCart(TestUser):
    def test_cart(self):
        super().test_success_registration()
        self.browser.find_element(By.CSS_SELECTOR, "#menu li:nth-child(2) a").click()

        self.browser.find_element(By.NAME, "in_stock").click()
        category_checkboxes = self.browser.find_elements(By.NAME, "category")
        for category_checkbox in category_checkboxes:
            category_checkbox.click()
        material_checkboxes = self.browser.find_elements(By.NAME, "material")
        for material_checkbox in material_checkboxes:
            material_checkbox.click()
        metal_checkboxes = self.browser.find_elements(By.NAME, "metal")
        for metal_checkbox in metal_checkboxes:
            self.browser.execute_script("arguments[0].click();", metal_checkbox)

        show_btn = self.browser.find_element(By.CSS_SELECTOR, "#filters button")
        self.browser.execute_script("arguments[0].click();", show_btn)

        some_jewelry = self.browser.find_element(By.CSS_SELECTOR, "#jewelries .card-item .card-footer a")
        self.browser.execute_script("arguments[0].click();", some_jewelry)

        add_into_cart_btn = self.browser.find_element(By.CSS_SELECTOR, "#view .price a")
        self.browser.execute_script("arguments[0].click();", add_into_cart_btn)

        self.browser.find_element(By.ID, "my_cart").click()
        order_btn = self.browser.find_element(By.CSS_SELECTOR, "#cart p a")
        order_btn.click()

        order_title = self.browser.find_element(By.TAG_NAME, "h6").text
        self.assertEqual(order_title, "Оформление заказа")

        self.browser.find_element(By.ID, "my_cart").click()
        remove_from_cart_btn = self.browser.find_element(By.CSS_SELECTOR, "#cart table a:nth-child(2)")
        remove_from_cart_btn.click()
        cart_text = self.browser.find_element(By.CSS_SELECTOR, "#cart p").text
        self.assertEqual(cart_text, "Пока товаров нет")

    def test_fail_cart(self):
        super().test_fail_registration()
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.CSS_SELECTOR, "#menu li:nth-child(2) a").click()

        self.browser.find_element(By.NAME, "in_stock").click()
        show_btn = self.browser.find_element(By.CSS_SELECTOR, "#filters button")
        self.browser.execute_script("arguments[0].click();", show_btn)

        some_jewelry = self.browser.find_element(By.CSS_SELECTOR, "#jewelries .card-item .card-footer a")
        self.browser.execute_script("arguments[0].click();", some_jewelry)

        add_into_cart_btn = self.browser.find_element(By.CSS_SELECTOR, "#view .price a")
        self.browser.execute_script("arguments[0].click();", add_into_cart_btn)

        authorization_title = self.browser.find_element(By.TAG_NAME, "h3").text
        self.assertEqual(authorization_title, "Авторизация")


class TestSimplePages(TestWalkPage):
    def test_pages(self):
        self.browser.get(self.live_server_url)

        # переход на страницу с оплатой
        self.browser.find_element(By.CSS_SELECTOR, "#menu li:nth-child(3) a").click()
        title_payment = self.browser.find_element(By.CSS_SELECTOR, "h6").text
        self.assertEqual(title_payment, 'Оплата')

        # переход на страницу с доставкой
        self.browser.find_element(By.CSS_SELECTOR, "#menu li:nth-child(4) a").click()
        title_delivery = self.browser.find_element(By.CSS_SELECTOR, "h6").text
        self.assertEqual(title_delivery, 'Доставка')

        # переход на страницу с о нас
        self.browser.find_element(By.CSS_SELECTOR, "#menu li:nth-child(5) a").click()
        title_about = self.browser.find_element(By.CSS_SELECTOR, "h6").text
        self.assertEqual(title_about, 'О нас')