import argparse
import json
import os
import random
import string
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from azure.identity import DeviceCodeCredential
from azure.mgmt.resource.resources import ResourceManagementClient
from azure.mgmt.resource.resources.models import ResourceGroup

BASE_DIR = Path(__file__).resolve().parent
DOCKERFILE = BASE_DIR / "aca" / "Dockerfile"
BACKEND_DIR = BASE_DIR.parent
LOCATION = "uaenorth"
DEFAULT_RG = "fipilot-rg"
ENV_NAME = "fipilot-aca-env"
APP_NAME = "smartresume-api"


def call(method: str, url: str, token: str, body=None):
    req = Request(url, method=method, headers={"Authorization": f"Bearer {token}"})
    if body is not None:
        req.data = json.dumps(body).encode()
        req.add_header("Content-Type", "application/json")
    try:
        with urlopen(req, timeout=180) as r:
            return r.status, json.loads(r.read().decode())
    except HTTPError as e:
        return e.code, e.read().decode()[:3000]


def get_credential(tenant_id):
    kwargs = {}
    tenant_id = tenant_id or os.environ.get("AZURE_TENANT_ID")
    if tenant_id:
        kwargs["tenant_id"] = tenant_id
    return DeviceCodeCredential(**kwargs)


def ensure_rg(client, rg: str, location: str) -> None:
    if client.resource_groups.check_existence(rg):
        print(f"Resource group '{rg}' exists")
        return
    client.resource_groups.create_or_update(rg, ResourceGroup(location=location))
    print(f"Created resource group '{rg}'")


def ensure_providers(client, namespaces) -> None:
    for ns in namespaces:
        try:
            state = client.providers.get(ns).registration_state
        except Exception:
            state = "Unknown"
        if state != "Registered":
            print(f"Registering provider '{ns}' ...")
            client.providers.register(ns)
    deadline = time.time() + 180
    while time.time() < deadline:
        ready = True
        for ns in namespaces:
            try:
                state = client.providers.get(ns).registration_state
            except Exception:
                state = "Unknown"
            if state != "Registered":
                ready = False
        if ready:
            print("All providers ready")
            return
        time.sleep(10)
    print("Warning: provider registration still pending")


def arm_deploy(token: str, subscription_id: str, rg: str, name: str, template: dict) -> None:
    url = (
        f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups/{rg}"
        f"/providers/Microsoft.Resources/deployments/{name}?api-version=2022-09-01"
    )
    body = {
        "properties": {
            "mode": "Incremental",
            "template": {
                "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
                "contentVersion": "1.0.0.0",
                "resources": template,
            },
            "parameters": {},
        }
    }
    print(f"ARM deployment '{name}' ...")
    status, resp = call("PUT", url, token, body=body)
    if status not in (200, 201):
        sys.exit(f"Deployment '{name}' request failed: {status} {resp}")

    while True:
        status, d = call("GET", url, token)
        state = d.get("properties", {}).get("provisioningState")
        if state in ("Succeeded", "Failed", "Canceled"):
            if state != "Succeeded":
                error = d.get("properties", {}).get("error", {})
                sys.exit(f"Deployment '{name}' failed: {json.dumps(error, indent=2)[:3000]}")
            print(f"Deployment '{name}' done")
            return
        time.sleep(10)


def main() -> None:
    parser = argparse.ArgumentParser(description="Deploy SmartResume to Azure Container Apps (scale-to-zero)")
    parser.add_argument("--subscription-id", default=None)
    parser.add_argument("--resource-group", default=DEFAULT_RG)
    parser.add_argument("--tenant-id", default=None)
    parser.add_argument("--image-tag", default="v1")
    args = parser.parse_args()

    subscription_id = args.subscription_id or os.environ.get("AZURE_SUBSCRIPTION_ID") or input("Subscription ID: ")
    credential = get_credential(args.tenant_id)
    token = credential.get_token("https://management.azure.com/.default").token
    rg = args.resource_group

    client = ResourceManagementClient(credential, subscription_id)
    ensure_rg(client, rg, LOCATION)
    ensure_providers(client, [
        "Microsoft.App",
        "Microsoft.ContainerRegistry",
        "Microsoft.OperationalInsights",
        "Microsoft.Insights",
        "Microsoft.Storage",
    ])

    # ---- 1. ACR (container registry) ----
    status, body = call(
        "GET",
        f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{rg}/providers/Microsoft.ContainerRegistry/registries?api-version=2023-07-01",
        token,
    )
    existing = body.get("value", []) if status == 200 else []
    if existing:
        acr_name = existing[0]["name"]
        print(f"Reusing existing ACR: {acr_name}")
    else:
        suffix = "".join(random.choices(string.ascii_lowercase, k=4))
        acr_name = f"fipilotacr{suffix}"
        arm_deploy(token, subscription_id, rg, f"deploy-acr-{acr_name}", [{
            "type": "Microsoft.ContainerRegistry/registries",
            "apiVersion": "2023-07-01",
            "name": acr_name,
            "location": LOCATION,
            "sku": {"name": "Basic"},
            "properties": {"adminUserEnabled": True},
        }])
    print(f"ACR: {acr_name}.azurecr.io")
    acr_id = f"/subscriptions/{subscription_id}/resourceGroups/{rg}/providers/Microsoft.ContainerRegistry/registries/{acr_name}"

    status, creds = call(
        "POST",
        f"https://management.azure.com{acr_id}/listCredentials?api-version=2023-07-01",
        token,
    )
    if status != 200:
        sys.exit(f"Failed to get ACR credentials: {status} {creds}")
    acr_username = creds["username"]
    acr_password = creds["passwords"][0]["value"]
    acr_server = f"{acr_name}.azurecr.io"

    # ---- 2. Build + push image ----
    image = f"{acr_server}/smartresume:{args.image_tag}"
    print(f"\n[docker] Building {image} (torch download, ~10-20 min) ...")
    subprocess.run(
        ["docker", "build", "-t", image, "-f", str(DOCKERFILE), str(BACKEND_DIR)],
        check=True,
    )
    print(f"[docker] Logging into {acr_server} ...")
    subprocess.run(
        ["docker", "login", acr_server, "-u", acr_username, "--password-stdin"],
        input=acr_password.encode(),
        check=True,
    )
    print(f"[docker] Pushing {image} (~3GB, a few minutes) ...")
    subprocess.run(["docker", "push", image], check=True)

    # ---- 3. Log Analytics workspace (for env logs) ----
    status, body = call(
        "GET",
        f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{rg}/providers/Microsoft.OperationalInsights/workspaces?api-version=2020-08-01",
        token,
    )
    if status != 200:
        sys.exit(f"Failed to list LA workspaces: {status} {body}")
    la_name = None
    la_customer_id = None
    for w in body.get("value", []):
        la_name = w["name"]
        la_customer_id = w["properties"]["customerId"]
        break
    if not la_name:
        la_name = f"fipilot-la-{suffix}"
        arm_deploy(token, subscription_id, rg, "deploy-la", [{
            "type": "Microsoft.OperationalInsights/workspaces",
            "apiVersion": "2020-08-01",
            "name": la_name,
            "location": LOCATION,
            "properties": {"sku": {"name": "PerGB2018"}, "retentionInDays": 30},
        }])
        status, w = call(
            "GET",
            f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{rg}/providers/Microsoft.OperationalInsights/workspaces/{la_name}?api-version=2020-08-01",
            token,
        )
        la_customer_id = w["properties"]["customerId"]
    status, keys = call(
        "POST",
        f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{rg}/providers/Microsoft.OperationalInsights/workspaces/{la_name}/sharedKeys?api-version=2020-08-01",
        token,
    )
    if status != 200:
        sys.exit(f"Failed to get LA keys: {status} {keys}")
    la_key = keys["primarySharedKey"]

    # ---- 4. Container Apps environment + app ----
    env_id = (
        f"/subscriptions/{subscription_id}/resourceGroups/{rg}"
        f"/providers/Microsoft.App/managedEnvironments/{ENV_NAME}"
    )
    arm_deploy(token, subscription_id, rg, "deploy-aca", [
        {
            "type": "Microsoft.App/managedEnvironments",
            "apiVersion": "2024-03-01",
            "name": ENV_NAME,
            "location": LOCATION,
            "properties": {
                "appLogsConfiguration": {
                    "destination": "log-analytics",
                    "logAnalyticsConfiguration": {
                        "customerId": la_customer_id,
                        "sharedKey": la_key,
                    },
                }
            },
        },
        {
            "type": "Microsoft.App/containerApps",
            "apiVersion": "2024-03-01",
            "name": APP_NAME,
            "location": LOCATION,
            "dependsOn": [f"microsoft.app/managedenvironments/{ENV_NAME}"],
            "properties": {
                "managedEnvironmentId": env_id,
                "configuration": {
                    "activeRevisionsMode": "Single",
                    "secrets": [{"name": "acr-pass", "value": acr_password}],
                    "registries": [
                        {
                            "server": acr_server,
                            "username": acr_username,
                            "passwordSecretRef": "acr-pass",
                        }
                    ],
                    "ingress": {
                        "external": True,
                        "targetPort": 8000,
                        "transport": "auto",
                    },
                },
                "template": {
                    "containers": [
                        {
                            "name": "smartresume",
                            "image": image,
                            "resources": {"cpu": 2.0, "memory": "4.0Gi"},
                            "probes": [
                                {
                                    "type": "Liveness",
                                    "httpGet": {"path": "/health", "port": 8000},
                                    "initialDelaySeconds": 60,
                                    "periodSeconds": 30,
                                }
                            ],
                        }
                    ],
                    "scale": {
                        "minReplicas": 0,
                        "maxReplicas": 2,
                        "rules": [
                            {
                                "name": "http-scale",
                                "http": {"metadata": {"concurrentRequests": "1"}},
                            }
                        ],
                    },
                },
            },
        },
    ])

    status, app = call(
        "GET",
        f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{rg}/providers/Microsoft.App/containerApps/{APP_NAME}?api-version=2024-03-01",
        token,
    )
    if status != 200:
        sys.exit(f"Failed to fetch app: {status} {app}")

    fqdn = app["properties"]["configuration"]["ingress"]["fqdn"]
    print("\n=== READY ===")
    print(f"OpenAI-compatible base_url: https://{fqdn}/v1")
    print(f"Health check:               https://{fqdn}/health")
    print("api_key: any value (no auth configured)")


if __name__ == "__main__":
    main()
