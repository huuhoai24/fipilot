import argparse
import os
import time
from pathlib import Path

from azure.ai.ml import MLClient
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import (
    DefaultScaleSettings,
    Environment,
    ManagedOnlineDeployment,
    ManagedOnlineEndpoint,
    Model,
    OnlineRequestSettings,
    Workspace,
)
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DeviceCodeCredential
from azure.mgmt.resource.resources import ResourceManagementClient
from azure.mgmt.resource.resources.models import ResourceGroup

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR.parent / "models" / "Qwen3-0.6B"
CONDA_FILE = BASE_DIR / "environment.yml"
SCORING_DIR = BASE_DIR / "scoring"
DEFAULT_ENDPOINT_NAME = "smartresume-qwen3-ep"
DEFAULT_DEPLOYMENT_NAME = "cpu-8vcore"
DEFAULT_INSTANCE_TYPE = "Standard_D8as_v4"
DEFAULT_LOCATION = "eastus"


def get_credential(tenant_id: str | None = None):
    kwargs = {}
    tenant_id = tenant_id or os.environ.get("AZURE_TENANT_ID")
    if tenant_id:
        kwargs["tenant_id"] = tenant_id
    return DeviceCodeCredential(**kwargs)


def resolve_subscription_id() -> str:
    provided = os.environ.get("AZURE_SUBSCRIPTION_ID")
    if provided:
        return provided
    return input("Enter your Azure subscription ID: ").strip()


def ensure_resource_group(client, resource_group: str, location: str) -> None:
    if client.resource_groups.check_existence(resource_group):
        print(f"Resource group '{resource_group}' already exists")
        return
    print(f"Creating resource group '{resource_group}' in {location} ...")
    client.resource_groups.create_or_update(resource_group, ResourceGroup(location=location))


def ensure_resource_providers(client) -> None:
    needed = [
        "Microsoft.MachineLearningServices",
        "Microsoft.ContainerRegistry",
        "Microsoft.OperationalInsights",
        "Microsoft.Insights",
        "Microsoft.Storage",
        "Microsoft.KeyVault",
        "Microsoft.Network",
    ]
    for ns in needed:
        try:
            state = client.providers.get(ns).registration_state
        except Exception:
            state = "Unknown"
        if state != "Registered":
            print(f"Registering resource provider '{ns}' (state: {state}) ...")
            client.providers.register(ns)

    deadline = time.time() + 180
    while time.time() < deadline:
        try:
            state = client.providers.get("Microsoft.MachineLearningServices").registration_state
        except Exception:
            state = "Unknown"
        if state == "Registered":
            print("All resource providers ready")
            return
        time.sleep(10)
    print("Warning: provider registration still pending, continuing anyway")


def ensure_workspace(ml_client: MLClient, workspace_name: str, location: str) -> None:
    try:
        ml_client.workspaces.get(workspace_name)
        print(f"Workspace '{workspace_name}' already exists")
        return
    except ResourceNotFoundError:
        pass
    print(f"Creating workspace '{workspace_name}' (takes a few minutes) ...")
    ml_client.workspaces.begin_create(
        Workspace(name=workspace_name, location=location)
    ).result()


def main() -> None:
    parser = argparse.ArgumentParser(description="Deploy SmartResume Qwen3-0.6B to an Azure ML Managed Online Endpoint")
    parser.add_argument("--subscription-id", default=None)
    parser.add_argument("--resource-group", default="fipilot-rg")
    parser.add_argument("--workspace-name", default="fipilot-ml")
    parser.add_argument("--endpoint-name", default=DEFAULT_ENDPOINT_NAME)
    parser.add_argument("--instance-type", default=DEFAULT_INSTANCE_TYPE)
    parser.add_argument("--location", default=DEFAULT_LOCATION)
    parser.add_argument("--tenant-id", default=None)
    args = parser.parse_args()

    credential = get_credential(args.tenant_id)
    subscription_id = args.subscription_id or resolve_subscription_id()

    rg_client = ResourceManagementClient(credential, subscription_id)
    ensure_resource_group(rg_client, args.resource_group, args.location)
    ensure_resource_providers(rg_client)

    ml_client = MLClient(credential, subscription_id, args.resource_group, args.workspace_name)
    ensure_workspace(ml_client, args.workspace_name, args.location)

    print(f"\nRegistering model from {MODEL_PATH} ...")
    model = ml_client.models.create_or_update(
        Model(
            name="SmartResume-Qwen3-06B",
            path=str(MODEL_PATH),
            type=AssetTypes.CUSTOM_MODEL,
            description="Alibaba-EI SmartResume Qwen3-0.6B (resume extraction fine-tune)",
        )
    )
    print(f"Model registered: {model.name} v{model.version}")

    print("Creating environment (CPU torch + transformers) ...")
    environment = ml_client.environments.create_or_update(
        Environment(
            name="smartresume-cpu-env",
            image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu22.04",
            conda_file=str(CONDA_FILE),
        )
    )
    print(f"Environment created: {environment.name} v{environment.version}")

    endpoint_name = args.endpoint_name
    try:
        ml_client.online_endpoints.get(endpoint_name)
        print(f"Endpoint '{endpoint_name}' already exists")
    except ResourceNotFoundError:
        print(f"Creating online endpoint '{endpoint_name}' ...")
        ml_client.online_endpoints.begin_create_or_update(
            ManagedOnlineEndpoint(name=endpoint_name, location=args.location, auth_mode="key")
        ).wait()

    deployment = ManagedOnlineDeployment(
        name=DEFAULT_DEPLOYMENT_NAME,
        endpoint_name=endpoint_name,
        model=model,
        environment=environment,
        instance_type=args.instance_type,
        instance_count=1,
        request_settings=OnlineRequestSettings(
            request_timeout_ms=90000,
            max_concurrent_requests_per_instance=2,
        ),
        scale_settings=DefaultScaleSettings(instance_count=1),
    )

    print(f"Creating deployment '{DEFAULT_DEPLOYMENT_NAME}' (env build + model load, ~15-25 min) ...")
    ml_client.online_deployments.begin_create_or_update(deployment).wait()
    print("Deployment created")

    endpoint = ml_client.online_endpoints.get(endpoint_name)
    endpoint.traffic = {DEFAULT_DEPLOYMENT_NAME: 100}
    ml_client.online_endpoints.begin_create_or_update(endpoint).wait()
    print("Traffic set to 100%")

    keys = ml_client.online_endpoints.get_keys(endpoint_name)
    print(f"\n=== READY ===")
    print(f"Scoring URI: {ml_client.online_endpoints.get(endpoint_name).scoring_uri}")
    print(f"Primary key: {keys.primary_key}")


if __name__ == "__main__":
    main()
