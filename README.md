# GetCxOneUsers

Exports all users from a Checkmarx One (CxOne) tenant to a CSV file using the [CheckmarxPythonSDK](https://github.com/checkmarx-ltd/checkmarx-python-sdk).

## Prerequisites

- Python 3.11+
- Access to a Checkmarx One tenant with sufficient permissions to list users (the `view-users` role)

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd GetCxOneUsers
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

### 4. Configure credentials

The SDK reads configuration from `~/.Checkmarx/config.ini` by default. Create the file if it does not exist:

```bash
mkdir -p ~/.Checkmarx
touch ~/.Checkmarx/config.ini
```

Add a `[CxOne]` section with your tenant details:

```ini
[CxOne]
access_control_url = https://<region>.iam.checkmarx.net
server             = https://<region>.ast.checkmarx.net
tenant_name        = <your-tenant-name>
grant_type         = refresh_token
client_id          = ast-app
refresh_token      = <your-api-key>
timeout            = 120
```

| Field                | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `access_control_url` | IAM base URL for your region (e.g. `https://sng.iam.checkmarx.net`)        |
| `server`             | API base URL for your region (e.g. `https://sng.ast.checkmarx.net`)        |
| `tenant_name`        | Your CxOne tenant name                                                      |
| `grant_type`         | Authentication method — use `refresh_token` for API key auth                |
| `client_id`          | OAuth client ID — `ast-app` for standard CxOne access                      |
| `refresh_token`      | Your CxOne API key (generated from the CxOne portal under **Access Management > API Keys**) |
| `timeout`            | HTTP request timeout in seconds                                             |

> **Alternative auth:** You can use `grant_type = password` with `username` and `password` fields instead of a refresh token, but API key authentication is recommended for scripts.

> **Alternative config locations:** You can also place credentials in `~/.Checkmarx/config.json`, set environment variables prefixed with `cxone_` (e.g. `cxone_tenant_name`), or pass `--cxone_tenant_name` on the command line.

## Running the script

```bash
python main.py
```

Sample output:

```
Realm: <tenant-name>
Total users: 42
Fetched 42/42
Written 42 users to users.csv
```

The script will create `users.csv` in the current directory.

## Output format

The CSV contains one row per user with the following columns:

| Column            | Description                                             |
|-------------------|---------------------------------------------------------|
| `id`              | Unique user ID (UUID)                                   |
| `username`        | Login username                                          |
| `first_name`      | First name                                              |
| `last_name`       | Last name                                               |
| `email`           | Email address                                           |
| `last_login`      | Timestamp of the most recent login (ISO 8601)           |
| `auth_provider`   | Authentication provider (`Application`, `SAML`, etc.)  |
| `creation_date`   | Account creation timestamp (epoch milliseconds)         |
| `is_enabled`      | Whether the account is active (`True` / `False`)        |
| `is_mfa_configured` | Whether MFA is enabled (`True` / `False`)             |
| `email_verified`  | Whether the email address has been verified             |
| `roles`           | Pipe-separated list of assigned roles                   |
| `groups`          | Pipe-separated list of assigned groups                  |
| `required_actions`| Pipe-separated list of pending required actions         |

Multi-value fields (`roles`, `groups`, `required_actions`) use `|` as a delimiter so the file remains valid CSV.

## Project structure

```
GetCxOneUsers/
├── main.py            # Main script
├── requirementst.txt  # Pinned dependency
├── venv/              # Virtual environment (not committed)
└── users.csv          # Output file (generated at runtime)
```
