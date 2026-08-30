import os
import pytest
import allure
from typing import Dict, Generator
from _pytest.fixtures import SubRequest
from custom_logger import console_logger, LogLevel
from pages.login import LoginPage
from playwright.sync_api import Page, Playwright, APIRequestContext

c_logger = console_logger(name="PyConf", level=LogLevel.DEBUG)

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)

@pytest.fixture(scope="function")
def browser_context_args(
    browser_context_args: Dict, request: SubRequest
):
    context_args = {
        **browser_context_args,
        "no_viewport": True
    }
    return context_args

@pytest.fixture(scope='session')
def sapi_context(
    playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    headers = {
        "Accept": "*/*"}
    request_context = playwright.request.new_context(
        base_url="http://localhost:3000",
        extra_http_headers=headers,
        timeout=0)
    yield request_context
    request_context.dispose()

@pytest.fixture(scope='session')
def sauceapi_context(
    playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    headers = {
        "Accept": "*/*",
        "Authorization": "Basic Base64{username:password}"}
    request_context = playwright.request.new_context(
        base_url="https://api.us-west-1.saucelabs.com",
        extra_http_headers=headers)
    yield request_context
    request_context.dispose()

def _get_env_var(varname: str) -> str:
    value = os.getenv(varname)
    assert value, f'{varname} is not set'
    return value

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call) :
    outcome = yield
    rep = outcome.get_result()
    c_logger.info(f'{rep.head_line} - {rep.failed}')
    if rep.when == 'call' and rep.failed:
        c_logger.error(rep.failed)
        page = item.funcargs.get("page")
        if page is not None:
            png_bytes = page.screenshot()
            allure.attach(
                png_bytes,
                name="full-page",
                attachment_type=allure.attachment_type.PNG
            )
