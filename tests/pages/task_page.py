class TaskPage:
    def __init__(self, page):
        self.page = page
        self.title = page.get_by_role("heading", name="Title", exact=True)
        self.delete_button = page.get_by_role("button", name="Delete", exact=True)

    def goto(self, task_id):
        self.page.goto(f"http://localhost:3456/tasks/{task_id}")

    def rename(self, new_title):
        self.title.click()
        self.title.fill(new_title)
        self.title.press("Enter")