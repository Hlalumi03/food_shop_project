import os
import unittest
from contextlib import redirect_stdout
from io import StringIO

os.environ["DATABASE_URL"] = "sqlite:///:memory:"


class RootEndpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from main import read_root
        from main import read_checkout
        from app.core.database import engine

        cls.read_root = staticmethod(read_root)
        cls.read_checkout = staticmethod(read_checkout)
        cls.engine = engine

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()

    def test_root_html_is_read_as_utf8(self):
        self.assertIn("Food Shop", self.read_root())

    def test_checkout_page_has_cart_summary_and_payment_form(self):
        page = self.read_checkout()

        self.assertIn('id="checkoutItems"', page)
        self.assertIn('id="totalAmount"', page)
        self.assertIn('id="checkoutForm"', page)

    def test_launcher_messages_are_windows_console_safe(self):
        from run import print_error, print_info, print_success, print_warning

        output = StringIO()
        with redirect_stdout(output):
            print_info("info")
            print_success("success")
            print_warning("warning")
            print_error("error")

        self.assertTrue(output.getvalue().isascii())


if __name__ == "__main__":
    unittest.main()
