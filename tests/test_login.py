from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage


def test_login(browser, test_user):
    context = browser.new_context()  # no saved session: log in for real
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(test_user["username"], test_user["password"])

    expect(HomePage(page).task_input).to_be_visible()
    context.close()