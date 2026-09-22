import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.mark.parametrize(
    "username, password",
    [
        pytest.param("valid_user", "DefinitelyNotThePassword1!", id="wrong password"),
        pytest.param("no_such_user_38f1c2", "AnyPassword1!", id="unknown username"),
    ],
)
def test_login_fails_with_invalid_credentials(browser, base_url, test_user, username, password):
    if username == "valid_user":
        username = test_user["username"]

    context = browser.new_context(base_url=base_url)
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(username, password)

    expect(login_page.error_message).to_be_visible()
    expect(HomePage(page).task_input).not_to_be_visible()

    context.close()