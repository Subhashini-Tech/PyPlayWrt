import json
import allure
import pytest
from jsonpath_ng import jsonpath, parse
from playwright.sync_api import APIRequestContext, expect, Page
from custom_logger import console_logger, LogLevel
c_logger = console_logger(name="test_api", level=LogLevel.DEBUG)

@pytest.mark.api
@allure.tag("api")
@allure.severity(allure.severity_level.CRITICAL)
def test_request_otp(
    sauceapi_context: APIRequestContext) -> None:
    allure.dynamic.title("Test Api")
    allure.dynamic.description("Get sauce build details")
    with allure.step("1. Http request - GET"):
        response = sauceapi_context.get(
            '/v2/builds/vdc?name=@test',
            ignore_https_errors= True
        )
    with allure.step("2. Validate response"):
        expect(response).to_be_ok()
        assert response.ok
        assert response.status == 200
    # builds = response.json()['builds'][0]['jobs']
    # c_logger.info(builds)
    with allure.step("3. Log data"):
        json_data = json.loads(response.text())
        match = parse('$.builds[0].name').find(json_data)
        c_logger.info(match[0].value)
