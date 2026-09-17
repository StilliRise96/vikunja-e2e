class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.get_by_role("textbox", name="Username Or Email Address", exact=True)
        self.password_input = page.get_by_role("textbox", name="Password", exact=True)
        self.login_button = page.get_by_role("button", name="Login", exact=True) 

    def goto(self):
        self.page.goto("http://localhost:3456/login")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        