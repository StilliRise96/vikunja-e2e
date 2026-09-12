from playwright.sync_api import expect

def test_login_and_create_task(page):
    page.goto("http://localhost:3456/login")
    page.fill("#username", "testuser")
    page.fill("#password", "testuser@1234") #has to be fixed in Phase 4
    page.get_by_role("button", name="Login").click()
    expect(page.get_by_placeholder("Add a task…")).to_be_visible()