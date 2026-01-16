# MCP Server Integration Test Suite

Please run the following tests for the MCP server tools and provide a summary at the end:

## Test 1: Device Lookup by MAC Address
**Objective:** Verify get_device tool retrieval
**Action:** Get device information for MAC address 7f:14:22:72:00:e5
**Expected Result:** Should return device details including vendor (Philips), model (Allura Xper X-Ray System), and device_uuid
**Validation Criteria:**
- Tool call succeeds
- Response contains MAC address 7f:14:22:72:00:e5
- Device type is X-Ray Machine
- vendor field is populated

## Test 2: Procedure History Retrieval
**Objective:** Verify get_procedures tool with device UUID
**Action:** Retrieve procedures for device_uuid: ffc20dfe-4c24-11ec-8a38-5eeeaabea551
**Expected Result:** Should return list of procedures with accession numbers, image counts, and timestamps
**Validation Criteria:**
- Tool call succeeds
- Returns multiple procedure records
- Each record has start/end times and procedure_name
- Image count is present for each procedure

## Test 3: Device Search with Filters
**Objective:** Verify search_for_devices tool with multiple parameters
**Action:** Search for devices with vendor "Philips" and device_type "X-Ray Machine"
**Expected Result:** Should return matching devices including the one from Test 1
**Validation Criteria:**
- Tool call succeeds
- Returns at least one device
- All returned devices match the search criteria

## Test 4: Vulnerability Query
**Objective:** Verify get_vulnerabilities tool with pagination
**Action:** Get vulnerabilities with severity "CRITICAL" and page_size 5
**Expected Result:** Should return paginated vulnerability list
**Validation Criteria:**
- Tool call succeeds
- Pagination metadata is present
- If vulnerabilities exist, severity filter is applied correctly

## Test 5: Subnet Listing
**Objective:** Verify get_subnets tool
**Action:** Get list of subnets with page_size 10
**Expected Result:** Should return subnet information
**Validation Criteria:**
- Tool call succeeds
- Returns subnet data with CIDR ranges if available

## Test 6: Threats Query
**Objective**: Verify get_threats tool with pagination
**Action**: Get all Medium threats with a page size of 3
**Expected Result:** Should return paginated threats list
**Validation Criteria:**
- Tool call succeeds
- Pagination metadata is present
- Only Medium threats are returned


---

## Test Execution Instructions:
1. Run each test sequentially
2. For each test, note: PASS/FAIL status and any error messages
3. After all tests complete, provide a summary table

## Summary Table Format:
| Test # | Test Name | Status | Duration | Notes |
|--------|-----------|--------|----------|-------|
| 1 | Device Lookup | PASS/FAIL | Xms | ... |
| 2 | Procedure History | PASS/FAIL | Xms | ... |
| 3 | Device Search | PASS/FAIL | Xms | ... |
| 4 | Vulnerability Query | PASS/FAIL | Xms | ... |
| 5 | Subnet Listing | PASS/FAIL | Xms | ... |

**Overall Result:** X/5 tests passed
**Integration Status:** HEALTHY/DEGRADED/FAILED
