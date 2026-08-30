import re
from playwright.sync_api import Page,expect
from custom_logger import console_logger, LogLevel
from typing import List

c_logger = console_logger(name="login", level=LogLevel.INFO)

class LoginPage:
    URL = 'http://localhost:3000'

    def __init__(self, page: Page) -> None:
        self.page = page

        # Locators (use modern selectors, no xpath)
        self.login_link = page.get_by_role("link", name="Login")
        self.email_input = page.get_by_placeholder("Email used to request OTP")
        self.otp_input = page.get_by_role("textbox", name="OTP")
        self.new_password_input = page.get_by_role("textbox", name="New Password")
        self.reset_button = page.get_by_role("button", name="Reset Password")
        self.success_message_text = page.get_by_text("Password reset successful.")

    def goto(self) -> None:
        self.page.goto(self.URL)

    def navigate_to_login(self) -> None:
        self.login_link.click()

    def reset_password(self, email: str, otp: str, password: str) -> None:
        self.email_input.fill(email)
        self.otp_input.fill(otp)
        self.new_password_input.fill(password)
        self.reset_button.click()

    def verify_success(self) -> None:
        expect(self.success_message_text).to_be_visible()
