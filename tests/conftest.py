import os
import uuid

import pytest
import requests
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage

BASE_URL = os.getenv("VIKUNJA_BASE_URL", "http://localhost:3456")


@pytest.fixture(scope="session")
def api_base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def test_user(api_base_url):
    """Create a fresh user through the API, once per test run."""
    suffix = uuid.uuid4().hex[:8]
    user = {
        "username": f"qa_{suffix}",
        "email": f"qa_{suffix}@example.com",
        "password": f"Qa@{suffix}1234",
    }
    response = requests.post(f"{api_base_url}/api/v1/register", json=user, timeout=10)
    assert response.ok, f"Register failed: {response.status_code} {response.text}"
    return user


@pytest.fixture(scope="session")
def logged_in_state(browser, test_user, tmp_path_factory):
    """Log in once through the UI and save the browser session to a file."""
    context = browser.new_context()
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
def api_token(api_base_url, test_user):
    """One API login per run, used for setting up test data."""
    response = requests.post(
        f"{api_base_url}/api/v1/login",
        json={"username": test_user["username"], "password": test_user["password"]},
        timeout=10,
    )
    assert response.ok, f"API login failed: {response.status_code} {response.text}"
    return response.json()["token"]


@pytest.fixture(scope="session")
def api_headers(api_token):
    return {"Authorization": f"Bearer {api_token}"}


@pytest.fixture(scope="session")
def project_id(api_base_url, api_headers):
    """The user's own Inbox project. Looked up, never hardcoded:
    each user gets a different id, and negative ids are virtual filters."""
    projects = requests.get(f"{api_base_url}/api/v1/projects", headers=api_headers, timeout=10).json()
    real = [p for p in projects if p["id"] > 0]
    assert real, f"No real project found: {projects}"
    return real[0]["id"]


@pytest.fixture
def api_task(api_base_url, api_headers, project_id):
    """Create a task through the API so UI tests start from a known state."""
    title = f"Task {uuid.uuid4().hex[:8]}"
    response = requests.put(
        f"{api_base_url}/api/v1/projects/{project_id}/tasks",
        json={"title": title},
        headers=api_headers,
        timeout=10,
    )
    assert response.status_code == 201, f"Task setup failed: {response.status_code} {response.text}"
    return response.json()