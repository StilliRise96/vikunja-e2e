from pages.task_page import TaskPage

def test_delete_task(page, api, api_task):
    task_page = TaskPage(page)
    task_page.goto(api_task["id"])

    task_page.delete()

    assert api.task_status_code(api_task["id"]) == 404, "Task still exists after delete"
