from __future__ import annotations

import argparse
import getpass
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass


@dataclass
class CheckResult:
    path: str
    status: int
    request_id: str


def request(base_url: str, path: str, token: str | None = None) -> CheckResult:
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request_object = urllib.request.Request(
        f"{base_url.rstrip('/')}{path}", headers=headers
    )
    try:
        with urllib.request.urlopen(request_object, timeout=30) as response:
            response.read()
            return CheckResult(
                path=path,
                status=response.status,
                request_id=response.headers.get("X-Request-ID", "<missing>"),
            )
    except urllib.error.HTTPError as error:
        error.read()
        return CheckResult(
            path=path,
            status=error.code,
            request_id=error.headers.get("X-Request-ID", "<missing>"),
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smoke test a deployed backend.")
    parser.add_argument("base_url", help="Cloud Run API base URL")
    parser.add_argument(
        "--token-env",
        default="FIREBASE_ID_TOKEN",
        help="Environment variable containing an optional Firebase ID token",
    )
    parser.add_argument(
        "--prompt-token",
        action="store_true",
        help="Prompt securely when the token environment variable is empty",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = os.getenv(args.token_env, "").strip()
    if not token and args.prompt_token:
        token = getpass.getpass("Firebase ID token (input hidden): ").strip()

    checks = [("/health", 200, None), ("/ready", 200, None)]
    checks.append(("/api/v2/auth/me", 200 if token else 401, token or None))
    failed = False
    for path, expected_status, request_token in checks:
        try:
            result = request(args.base_url, path, request_token)
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            print(json.dumps({"path": path, "error": type(error).__name__}))
            failed = True
            continue
        print(
            json.dumps(
                {
                    "path": result.path,
                    "status": result.status,
                    "expected": expected_status,
                    "request_id": result.request_id,
                }
            )
        )
        failed = failed or result.status != expected_status
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
