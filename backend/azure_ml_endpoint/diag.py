import argparse

from azure.identity import DeviceCodeCredential
from azure.mgmt.resource.resources import ResourceManagementClient


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subscription-id", required=True)
    args = parser.parse_args()
    sub_id = args.subscription_id

    cred = DeviceCodeCredential()
    token = cred.get_token("https://management.azure.com/.default")
    print("Token OK")
    for attr in ("tenant_id", "account_id", "expires_on"):
        if hasattr(token, attr):
            print(f"  {attr}: {getattr(token, attr)}")

    client = ResourceManagementClient(cred, sub_id)
    try:
        subs = list(client.subscriptions.list())
        print("\nSubscriptions visible to this account:")
        for s in subs:
            print(f"  - {s.subscription_id}  {s.display_name}  state={s.state}")
        target = [s for s in subs if s.subscription_id == sub_id]
        if target:
            print(f"\nTarget subscription IS visible: {target[0].display_name}")
        else:
            print(f"\n[!] Target subscription {sub_id} NOT in the list above")
    except Exception as e:
        print(f"\n[!] Cannot list subscriptions: {type(e).__name__}: {e}")

    try:
        client.resource_groups.check_existence("fipilot-rg")
        print("check_existence fipilot-rg: OK")
    except Exception as e:
        print(f"\n[!] check_existence failed: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
