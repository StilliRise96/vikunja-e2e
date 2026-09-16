from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.home_page import HomePage


def test_login(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("testuser", "testuser@1234")  # hardcoded password: fix in Phase 4

    home_page = HomePage(page)
    expect(home_page.task_input).to_be_visible()