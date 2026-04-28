# Cylera MCP Server Organization Switching Test Suite

## Prerequisites

Before running these tests, ensure the Cylera MCP Server is installed and configured with the required secrets. The full installation instructions are available in the [README](https://github.com/Cylera/cylera-mcp-server#installation).

### Required Secrets

The following environment variables must be configured, either via a `.env` file in the cloned MCP server directory or via [Doppler](https://www.doppler.com) or some other secrets manager:

| Variable | Description |
|---|---|
| `CYLERA_BASE_URL` | Your Cylera Partner API base URL (e.g. `https://partner.demo.cylera.com`) |
| `CYLERA_USERNAME` | Your Cylera username |
| `CYLERA_PASSWORD` | Your Cylera password |
|                   |                                                              |
|                   |                                                              |
|                   |                                                              |

> ⚠️ **Access required:** If you do not have credentials for the test environment, please reach out to the primary author to request access to these secrets.

### Expected Test Environment

The test cases in this file were recorded against the **Cylera demo environment** (`partner.demo.cylera.com`) using a specific account. Results will differ if run against a different environment and/or using a different account. 

---

## Test Format

Each test specifies a **prompt**, the **expected JSON response**, and the **assertion type**.

---

## Test Cases

### TC-001 — Reset Organization

**Prompt:**
```
Reset my organization
```

**Tool Called:** `reset_organization`

**Expected Response (Exact JSON Match):**
```json
{"message":"Organization reset queued successfully"}
```

**Assertion:** `exact_json_match`

---

### TC-002 — Switch Organization

**Prompt:**
```
Switch to Cylera
```

**Tools Called:** `get_available_organizations` → `switch_organization`

**Expected Response (Exact JSON Match):**
```json
{"organization_id": 17, "name": "Cylera", "internal_name": "cylera"}
```

**Assertion:** `exact_json_match`

---

### TC-003 — Get Current Organization

**Prompt:**
```
Get my current organization and make sure it is "Cylera".
```

**Tool Called:** `get_organization`

**Expected Response (Exact JSON Match):**
```json
{"organization_id": 17, "name": "Cylera", "internal_name": "cylera"}
```

**Assertion:** `exact_json_match` — assert `name == "Cylera"`

---

### TC-004 — Reset Organization

**Prompt:**
```
Reset organization
```

**Tool Called:** `reset_organization`

**Expected Response (Exact JSON Match):**
```json
{"message":"Organization reset queued successfully"}
```

**Assertion:** `exact_json_match`

---
