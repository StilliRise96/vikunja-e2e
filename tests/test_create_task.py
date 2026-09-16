import uuid

from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.home_page import HomePage


def test_create_task(page):
    title = f"Buy Bike {uuid.uuid4().hex[:8]}"

    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("testuser", "testuser@1234")  # hardcoded password: fix in Phase 4

    home_page = HomePage(page)
    home_page.add_task(title)

    expect(home_page.task_link(title)).to_be_visible()