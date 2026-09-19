import uuid

from playwright.sync_api import expect

from pages.home_page import HomePage


def test_create_task(page):
    home_page = HomePage(page)
    page.goto("http://localhost:3456/")

    title = f"Buy Bike {uuid.uuid4().hex[:8]}"
    home_page.add_task(title)

    expect(home_page.task_link(title)).to_be_visible()