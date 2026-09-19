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