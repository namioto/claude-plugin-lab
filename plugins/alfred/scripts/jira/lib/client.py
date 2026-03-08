"""Jira REST API 공용 클라이언트"""

import os
import sys

import requests


class JiraError(Exception):
    """Jira API 호출 실패 시 발생하는 예외"""

    def __init__(self, status_code: int, text: str):
        self.status_code = status_code
        self.text = text
        super().__init__(f"Jira API error {status_code}: {text}")


class JiraClient:
    """환경변수 기반 인증을 처리하는 Jira HTTP 클라이언트"""

    def __init__(self):
        email = os.environ.get("JIRA_EMAIL")
        api_key = os.environ.get("JIRA_API_KEY")
        base_url = os.environ.get("ATLASSIAN_URL", "").rstrip("/")
        if not email or not api_key or not base_url:
            print(
                "Error: JIRA_EMAIL, JIRA_API_KEY, ATLASSIAN_URL environment variables are required",
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = base_url
        self._auth = (email, api_key)

    def get(self, path: str, params: dict | None = None) -> dict | list:
        resp = requests.get(
            f"{self.base_url}{path}",
            params=params,
            auth=self._auth,
            headers={"Accept": "application/json"},
        )
        if not resp.ok:
            raise JiraError(resp.status_code, resp.text)
        return resp.json()

    def post(self, path: str, payload: dict) -> dict | None:
        resp = requests.post(
            f"{self.base_url}{path}",
            json=payload,
            auth=self._auth,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        if not resp.ok:
            raise JiraError(resp.status_code, resp.text)
        # POST /transitions 는 204 No Content 반환
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()

    def put(self, path: str, payload: dict) -> dict | None:
        resp = requests.put(
            f"{self.base_url}{path}",
            json=payload,
            auth=self._auth,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        if not resp.ok:
            raise JiraError(resp.status_code, resp.text)
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()
