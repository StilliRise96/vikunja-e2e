import uuid

from playwright.sync_api import expect

from pages.task_page import TaskPage


def test_rename_task(page, api_task):
    task_page = TaskPage(page)
    task_page.goto(api_task["id"])

    new_title = f"Renamed {uuid.uuid4().hex[:8]}"
    task_page.rename(new_title)
    page.wait_for_timeout(500)  # temporary

    page.reload()

    expect(task_page.title).to_have_text(new_title)