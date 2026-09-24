import requests


class VikunjaApi:
    """Talks to the Vikunja REST API so tests and fixtures don't build HTTP requests."""

    TIMEOUT = 10

    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.token = token

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def _url(self, path):
        return f"{self.base_url}/api/v1{path}"

    def register(self, username, email, password):
        response = requests.post(
            self._url("/register"),
            json={"username": username, "email": email, "password": password},
            timeout=self.TIMEOUT,
        )
        assert response.ok, f"Register failed: {response.status_code} {response.text}"
        return response.json()

    def login(self, username, password):
        response = requests.post(
            self._url("/login"),
            json={"username": username, "password": password},
            timeout=self.TIMEOUT,
        )
        assert response.ok, f"API login failed: {response.status_code} {response.text}"
        self.token = response.json()["token"]
        return self.token

    def first_project_id(self):
        """The user's own Inbox. Looked up, never hardcoded: each user gets a
        different id, and negative ids are virtual filters, not real projects."""
        response = requests.get(self._url("/projects"), headers=self.headers, timeout=self.TIMEOUT)
        assert response.ok, f"Could not list projects: {response.status_code} {response.text}"
        real = [p for p in response.json() if p["id"] > 0]
        assert real, f"No real project found: {response.text}"
        return real[0]["id"]

    def create_task(self, project_id, title):
        response = requests.put(
            self._url(f"/projects/{project_id}/tasks"),
            json={"title": title},
            headers=self.headers,
            timeout=self.TIMEOUT,
        )
        assert response.status_code == 201, f"Task setup failed: {response.status_code} {response.text}"
        return response.json()

    def task_status_code(self, task_id):
        """Status code only: used to check whether a task still exists."""
        response = requests.get(self._url(f"/tasks/{task_id}"), headers=self.headers, timeout=self.TIMEOUT)
        return response.status_code