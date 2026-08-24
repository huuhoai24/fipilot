import argparse
import json
import os
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from azure.identity import DeviceCodeCredential


def call(url: str, token: str):
    req = Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode())
    except HTTPError as e:
        return e.code, e.read().decode()[:1000]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subscription-id", required=True)
    parser.add_argument("--tenant-id", default=None)
    args = parser.parse_args()

    kwargs = {}
    tenant_id = args.tenant_id or os.environ.get("AZURE_TENANT_ID")
    if tenant_id:
        kwargs["tenant_id"] = tenant_id

    cred = DeviceCodeCredential(**kwargs)
    token = cred.get_token("https://management.azure.com/.default").token

    status, body = call(
        f"https://management.azure.com/subscriptions/{args.subscription_id}"
        "/providers/Microsoft.Authorization/policyAssignments?api-version=2022-06-01",
        token,
    )
    print(f"Policy assignments: HTTP {status}")
    if status != 200:
        print(" body:", body)
        return

    for a in body.get("value", []):
        props = a.get("properties", {})
        pid = props.get("policyDefinitionId", "")
        if "e56962a6-4747-49cd-b67b-bf8b01975c4c" in pid or "locations" in pid.lower():
            params = props.get("parameters", {})
            allowed = params.get("listOfAllowedLocations", {}).get("value", [])
            print("ALLOWED LOCATIONS:", ", ".join(allowed))
            return

    print("No location-restriction policy found. Assignments:")
    for a in body.get("value", []):
        print(" -", a.get("properties", {}).get("policyDefinitionId", ""))


if __name__ == "__main__":
    main()
