import csv
import json
from pathlib import Path

from CheckmarxPythonSDK.CxOne.accessControlAPI import AccessControlAPI
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.configuration import Configuration

TENANTS_CONFIG = "tenants.json"
PAGE_SIZE = 100

CSV_FIELDS = [
    "id", "username", "first_name", "last_name", "email",
    "last_login", "auth_provider", "creation_date",
    "is_enabled", "is_mfa_configured", "email_verified",
    "roles", "groups", "required_actions",
]


def build_configuration(tenant: dict) -> Configuration:
    iam_url = tenant.get("access_control_url", "https://iam.checkmarx.net").rstrip("/")
    tenant_name = tenant["tenant_name"]
    return Configuration(
        server_base_url=tenant.get("server", "https://ast.checkmarx.net"),
        iam_base_url=iam_url,
        token_url=f"{iam_url}/auth/realms/{tenant_name}/protocol/openid-connect/token",
        tenant_name=tenant_name,
        grant_type=tenant.get("grant_type", "refresh_token"),
        client_id=tenant.get("client_id", "ast-app"),
        client_secret=tenant.get("client_secret"),
        api_key=tenant.get("refresh_token"),
        username=tenant.get("username"),
        password=tenant.get("password"),
        timeout=int(tenant.get("timeout", 60)),
        verify=tenant.get("verify", True),
        cert=tenant.get("cert"),
        proxies={
            "http": tenant.get("proxy"),
            "https": tenant.get("proxy"),
        },
        logging_level=tenant.get("logging_level", "INFO"),
        max_retries=int(tenant.get("max_retries", 3)),
        rate_limit_capacity=int(tenant.get("rate_limit_capacity", 20000)),
        rate_limit_period=int(tenant.get("rate_limit_period", 300)),
        rate_limit_refill_rate=float(tenant.get("rate_limit_refill_rate")) if tenant.get("rate_limit_refill_rate") else None,
    )


def fetch_all_users(api: AccessControlAPI, realm: str):
    total = api.get_users_count(realm=realm)
    print(f"  Total users: {total}")

    users = []
    offset = 0
    while offset < total:
        batch = api.get_users(realm=realm, first=offset, max_result_size=PAGE_SIZE)
        if not batch:
            break
        users.extend(batch)
        offset += len(batch)
        print(f"  Fetched {offset}/{total}")

    return users


def write_csv(users, output_file: str):
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for user in users:
            writer.writerow({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "last_login": user.last_login,
                "auth_provider": user.auth_provider,
                "creation_date": user.creation_date,
                "is_enabled": user.is_enabled,
                "is_mfa_configured": user.is_mfa_configured,
                "email_verified": user.email_verified,
                "roles": "|".join(user.roles) if user.roles else "",
                "groups": "|".join(user.groups) if user.groups else "",
                "required_actions": "|".join(user.required_actions) if user.required_actions else "",
            })
    print(f"  Written {len(users)} users to {output_file}")


if __name__ == "__main__":
    config_path = Path(TENANTS_CONFIG)
    if not config_path.exists():
        print(f"Config file '{TENANTS_CONFIG}' not found. Copy tenants.json.example to tenants.json and fill in your credentials.")
        raise SystemExit(1)

    with open(config_path, encoding="utf-8") as f:
        tenants = json.load(f)

    for tenant in tenants:
        tenant_name = tenant["tenant_name"]
        print(f"\nProcessing tenant: {tenant_name}")
        configuration = build_configuration(tenant)
        api_client = ApiClient(configuration=configuration)
        api = AccessControlAPI(api_client=api_client)
        users = fetch_all_users(api, realm=tenant_name)
        write_csv(users, f"users_{tenant_name}.csv")
