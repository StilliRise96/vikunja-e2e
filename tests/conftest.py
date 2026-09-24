import uuid

import pytest
from playwright.sync_api import expect

from api.vikunja_api import VikunjaApi
from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def api_base_url(base_url):
    return base_url


@pytest.fixture(scope="session")
def api(api_base_url):
    return VikunjaApi(api_base_url)


@pytest.fixture(scope="session")
def test_user(api):
    """Create a fresh user through the API, once per test run."""
    suffix = uuid.uuid4().hex[:8]
    user = {
        "username": f"qa_{suffix}",
        "email": f"qa_{suffix}@example.com",
        "password": f"Qa@{suffix}1234",
    }
    api.register(**user)
    api.login(user["username"], user["password"])
    return user


@pytest.fixture(scope="session")
def logged_in_state(browser, base_url, test_user, tmp_path_factory):
    """Log in once through the UI and save the browser session to a file."""
    context = browser.new_context(base_url=base_url)
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(test_user["username"], test_user["password"])
    expect(HomePage(page).task_input).to_be_visible()

    state_path = tmp_path_factory.mktemp("state") / "storage_state.json"
    context.storage_state(path=state_path)
    context.close()
    return str(state_path)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, logged_in_state):
    """Every test's browser starts from the saved logged-in session."""
    return {**browser_context_args, "storage_state": logged_in_state}


@pytest.fixture(scope="session")
def project_id(api, test_user):
    return api.first_project_id()


@pytest.fixture
def api_task(api, project_id):
    """Create a task through the API so UI tests start from a known state."""
    return api.create_task(project_id, f"Task {uuid.uuid4().hex[:8]}")