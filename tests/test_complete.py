from playwright.sync_api import expect

from pages.home_page import HomePage


def test_mark_task_as_done(page, api_task):
    home_page = HomePage(page)
    page.goto("http://localhost:3456/")

    checkbox = home_page.task_checkbox(api_task["title"])
    expect(checkbox).not_to_be_checked()

    home_page.mark_done(api_task["title"])

    expect(checkbox).to_be_checked()