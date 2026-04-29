import csv
from CheckmarxPythonSDK.CxOne.accessControlAPI import get_users, get_users_count
from CheckmarxPythonSDK.CxOne.config import construct_configuration

OUTPUT_FILE = "users.csv"
PAGE_SIZE = 100

CSV_FIELDS = [
    "id", "username", "first_name", "last_name", "email",
    "last_login", "auth_provider", "creation_date",
    "is_enabled", "is_mfa_configured", "email_verified",
    "roles", "groups", "required_actions",
]


def fetch_all_users(realm: str):
    total = get_users_count(realm=realm)
    print(f"Total users: {total}")

    users = []
    offset = 0
    while offset < total:
        batch = get_users(realm=realm, first=offset, max_result_size=PAGE_SIZE)
        if not batch:
            break
        users.extend(batch)
        offset += len(batch)
        print(f"Fetched {offset}/{total}")

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
    print(f"Written {len(users)} users to {output_file}")


if __name__ == "__main__":
    config = construct_configuration()
    realm = config.tenant_name
    print(f"Realm: {realm}")

    users = fetch_all_users(realm=realm)
    write_csv(users, OUTPUT_FILE)
