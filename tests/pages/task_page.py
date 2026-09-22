class TaskPage:
    def __init__(self, page):
        self.page = page
        self.task_id = None
        self.title = page.get_by_role("heading", name="Title", exact=True)
        self.delete_button = page.get_by_role("button", name="Delete", exact=True)
        self.delete_dialog = page.get_by_role("dialog", name="Delete this task")
        self.confirm_delete_button = self.delete_dialog.get_by_role("button", name="Do it!", exact=True)

    def goto(self, task_id):
        self.task_id = task_id
        self.page.goto(f"/tasks/{task_id}")

    def rename(self, new_title):
        self.title.click()
        self.title.fill(new_title)
        with self.page.expect_response(self._is_write_to_this_task) as response_info:
            self.title.press("Enter")
        assert response_info.value.ok, f"Save failed: {response_info.value.status}"

    def delete(self):
        self.delete_button.click()
        with self.page.expect_response(self._is_write_to_this_task) as response_info:
            self.confirm_delete_button.click()
        assert response_info.value.ok, f"Delete failed: {response_info.value.status}"

    def _is_write_to_this_task(self, response):
        return (response.url.endswith(f"/api/v1/tasks/{self.task_id}")
                and response.request.method != "GET")