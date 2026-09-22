import requests

from pages.task_page import TaskPage


def test_delete_task(page, api_task, api_base_url, api_headers):
    task_page = TaskPage(page)
    task_page.goto(api_task["id"])

    task_page.delete()

    response = requests.get(f"{api_base_url}/api/v1/tasks/{api_task['id']}", headers=api_headers, timeout=10)
    assert response.status_code == 404, f"Task still exists: {response.status_code} {response.text}"