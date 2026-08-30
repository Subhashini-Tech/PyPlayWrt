import pytest
from playwright.sync_api import Page, expect, APIRequestContext
from pages.login import LoginPage
import allure
from custom_logger import console_logger, LogLevel

c_logger = console_logger(name="feature_goals", level=LogLevel.DEBUG)

testEmail = [
    'test@gmail.com',
    # 'MX'
]

@pytest.mark.smoke
@allure.tag("login")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize('email', testEmail)
def test_Verify_user_able_to_reset_password(page: Page,
    email: str,
    login_page : LoginPage,
    sapi_context: APIRequestContext) -> None:
    allure.dynamic.title(f'Verify_user_able_to_reset_password {email}')
    with allure.step("1. REQUEST OTP"):
        response = sapi_context.post(
            "http://localhost:3000/api/request-otp",
            headers={
                "Content-Type": "application/json"
            },
            data={
                "email": f"{email}"
            }
        )
        assert response.status == 200
        otp = response.json()['otp']
        c_logger.info(f'{otp} - {email}')
    with allure.step("2. Open Page"):
        login_page.goto()
    with allure.step("3. Navigate to login page"):
        login_page.navigate_to_login()
    with allure.step("4. Verify user can reset password"):
        login_page.reset_password(email, otp, "test")
    with allure.step("5. Verify success message"):
        login_page.verify_success()
