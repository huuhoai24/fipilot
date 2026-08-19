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
        return e.code, e.read().decode()[:500]


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
        "https://management.azure.com/subscriptions?api-version=2022-12-01", token
    )
    print(f"List ALL subscriptions I can access: HTTP {status}")
    if status == 200:
        for s in body.get("value", []):
            print(f"  - {s['subscriptionId']}  {s.get('displayName')}  state={s.get('state')}")
        found = any(s["subscriptionId"] == args.subscription_id for s in body.get("value", []))
        print(">> Target subscription in this list:", found)
    else:
        print("  body:", body)

    status, body = call(
        f"https://management.azure.com/subscriptions/{args.subscription_id}?api-version=2022-12-01",
        token,
    )
    print(f"\nGet target subscription directly: HTTP {status}")
    if status == 200:
        print(
            f"  displayName: {body.get('displayName')} | tenantId: {body.get('tenantId')}"
            f" | state: {body.get('state')}"
        )
    else:
        print("  body:", body)


if __name__ == "__main__":
    main()
