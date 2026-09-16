class HomePage:
    def __init__(self, page):
        self.page = page
        self.task_input = page.get_by_placeholder("Add a task…")
        self.add_button = page.get_by_role("button", name="Add", exact=True)

    def add_task(self, title):
        self.task_input.fill(title)
        self.add_button.click()

    def task_link(self, title):
        return self.page.get_by_role("link", name=title, exact=True)