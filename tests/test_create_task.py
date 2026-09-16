from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.home_page import HomePage
import uuid

def test_create_task(page):
    login_page = LoginPage(page)
    login_page.goto()
    title = f"Buy Bike {uuid.uuid4().hex[:8]}"
    login_page.login("testuser", "testuser@1234")  # hardcoded password: fix in Phase 4
    home_page = HomePage(page)
    home_page.add_task(title)

    expect(page.get_by_role("link", name=title)).to_be_visible()