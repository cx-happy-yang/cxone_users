# cxone_users

Exports all users from one or more Checkmarx One (CxOne) tenants to CSV files using the [CheckmarxPythonSDK](https://github.com/checkmarx-ltd/checkmarx-python-sdk). A separate CSV file is created for each tenant.

## Prerequisites

- Python 3.11+
- Access to each CxOne tenant with sufficient permissions to list users (the `view-users` role)

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd cxone_users
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install CheckmarxPythonSDK==1.8.1
```

### 4. Configure tenants

Copy the example config and fill in your credentials:

```bash
cp tenants.json.example tenants.json
```

`tenants.json` is a JSON array — add one object per tenant:

```json
[
  {
    "access_control_url": "https://sng.iam.checkmarx.net",
    "server": "https://sng.ast.checkmarx.net",
    "tenant_name": "my-tenant",
    "grant_type": "refresh_token",
    "client_id": "ast-app",
    "refresh_token": "<api-key>",
    "timeout": 120
  }
]
```

| Field                | Required | Description                                                                                      |
|----------------------|----------|--------------------------------------------------------------------------------------------------|
| `tenant_name`        | Yes      | Your CxOne tenant name                                                                           |
| `access_control_url` | Yes      | IAM base URL for your region (e.g. `https://sng.iam.checkmarx.net`)                             |
| `server`             | Yes      | API base URL for your region (e.g. `https://sng.ast.checkmarx.net`)                             |
| `grant_type`         | No       | Auth method — `refresh_token` (default) or `password`                                           |
| `client_id`          | No       | OAuth client ID — defaults to `ast-app`                                                         |
| `refresh_token`      | No*      | CxOne API key — generated from **Access Management > API Keys** in the portal                   |
| `username`           | No*      | Username for `password` grant type                                                               |
| `password`           | No*      | Password for `password` grant type                                                               |
| `client_secret`      | No       | Client secret if required by your tenant                                                         |
| `timeout`            | No       | HTTP request timeout in seconds (default: `60`)                                                  |
| `verify`             | No       | TLS verification — `true` (default) or `false`                                                   |
| `proxy`              | No       | HTTP/HTTPS proxy URL                                                                             |
| `logging_level`      | No       | SDK log level: `DEBUG`, `INFO`, `WARNING`, `ERROR` (default: `INFO`)                            |

\* Provide either `refresh_token` **or** `username` + `password` depending on your `grant_type`.

> **Note:** `tenants.json` is excluded from version control by `.gitignore` because it contains credentials. Never commit it.

## Running the script

```bash
python main.py
```

Sample output for two tenants:

```
Processing tenant: tenant-one
  Total users: 42
  Fetched 42/42
  Written 42 users to users_tenant-one.csv

Processing tenant: tenant-two
  Total users: 17
  Fetched 17/17
  Written 17 users to users_tenant-two.csv
```

One CSV file is created per tenant in the current directory.

## Output format

Each CSV file contains one row per user with the following columns:

| Column               | Description                                             |
|----------------------|---------------------------------------------------------|
| `id`                 | Unique user ID (UUID)                                   |
| `username`           | Login username                                          |
| `first_name`         | First name                                              |
| `last_name`          | Last name                                               |
| `email`              | Email address                                           |
| `last_login`         | Timestamp of the most recent login (ISO 8601)           |
| `auth_provider`      | Authentication provider (`Application`, `SAML`, etc.)  |
| `creation_date`      | Account creation timestamp (epoch milliseconds)         |
| `is_enabled`         | Whether the account is active (`True` / `False`)        |
| `is_mfa_configured`  | Whether MFA is enabled (`True` / `False`)               |
| `email_verified`     | Whether the email address has been verified             |
| `roles`              | Pipe-separated list of assigned roles                   |
| `groups`             | Pipe-separated list of assigned groups                  |
| `required_actions`   | Pipe-separated list of pending required actions         |

Multi-value fields (`roles`, `groups`, `required_actions`) use `|` as a delimiter so the file remains valid CSV.

## Project structure

```
cxone_users/
├── main.py                 # Main script
├── tenants.json.example    # Example tenant config (copy to tenants.json)
├── tenants.json            # Your tenant credentials (git-ignored)
├── requirementst.txt       # Pinned dependency
├── venv/                   # Virtual environment (not committed)
└── users_<tenant>.csv      # Output files (generated at runtime, git-ignored)
```
