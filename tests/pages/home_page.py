class HomePage:
    def __init__(self, page):
        self.page = page

    def add_task(self, title):
        self.page.get_by_placeholder("Add a task…").fill(title)
        self.page.get_by_role("button", name="Add", exact=True).click()