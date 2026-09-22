class TaskPage:
    def __init__(self, page):
        self.page = page
        self.task_id = None
        self.title = page.get_by_role("heading", name="Title", exact=True)
        self.delete_button = page.get_by_role("button", name="Delete", exact=True)

    def goto(self, task_id):
        self.task_id = task_id
        self.page.goto(f"http://localhost:3456/tasks/{task_id}")

    def rename(self, new_title):
        self.title.click()
        self.title.fill(new_title)
        with self.page.expect_response(self._is_save_of_this_task) as response_info:
            self.title.press("Enter")
        assert response_info.value.ok, f"Save failed: {response_info.value.status}"

    def _is_save_of_this_task(self, response):
        return (response.url.endswith(f"/api/v1/tasks/{self.task_id}")
                and response.request.method != "GET")