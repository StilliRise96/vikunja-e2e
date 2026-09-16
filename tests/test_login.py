from playwright.sync_api import expect
from pages.login_page import LoginPage


def test_login(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("testuser", "testuser@1234")  # hardcoded password: fix in Phase 4

    expect(page.get_by_placeholder("Add a task…")).to_be_visible()