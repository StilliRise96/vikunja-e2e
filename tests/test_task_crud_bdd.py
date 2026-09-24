import uuid

from playwright.sync_api import expect
from pytest_bdd import given, scenarios, then, when

from pages.home_page import HomePage
from pages.task_page import TaskPage

scenarios("features/task_crud.feature")


# ---------- Given ----------

@given("I am on my task list")
def open_task_list(page):
    page.goto("/")


@given("a task exists", target_fixture="task")
def existing_task(api_task):
    return api_task


@given("the task is not done")
def task_not_done(page, task):
    expect(HomePage(page).task_checkbox(task["title"])).not_to_be_checked()


# ---------- When ----------

@when("I add a task with a unique title", target_fixture="title")
def add_task(page):
    title = f"BDD Task {uuid.uuid4().hex[:8]}"
    HomePage(page).add_task(title)
    return title


@when("I rename the task", target_fixture="new_title")
def rename_task(page, task):
    task_page = TaskPage(page)
    task_page.goto(task["id"])
    new_title = f"Renamed {uuid.uuid4().hex[:8]}"
    task_page.rename(new_title)
    return new_title


@when("I mark the task as done")
def mark_task_done(page, task):
    HomePage(page).mark_done(task["title"])


@when("I delete the task")
def delete_task(page, task):
    task_page = TaskPage(page)
    task_page.goto(task["id"])
    task_page.delete()


# ---------- Then ----------

@then("the task appears in my task list")
def task_in_list(page, title):
    expect(HomePage(page).task_link(title)).to_be_visible()


@then("the new title is still shown after a reload")
def title_saved(page, new_title):
    page.reload()
    expect(TaskPage(page).title).to_have_text(new_title)


@then("the task is marked as done")
def task_is_done(page, task):
    expect(HomePage(page).task_checkbox(task["title"])).to_be_checked()


@then("the task no longer exists")
def task_is_gone(task, api):
    assert api.task_status_code(task["id"]) == 404, "Task still exists after delete"