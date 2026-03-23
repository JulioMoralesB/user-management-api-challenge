# User Management API - E2E Test Suite

End-to-end tests for the User Management API, covering both **dev** and **prod** environments.

## Test Results

Test results are available in multiple places after each workflow run:

- **GitHub Actions Summary** — Open the workflow run and check the **Summary** tab for a quick overview of passed/failed tests and a link to the full HTML report.
- **HTML Reports (GitHub Pages)** — Detailed interactive reports are published automatically:
  - [Index Page](https://juliomoralesb.github.io/user-management-api-challenge/) — links to both environment reports.
  - [Dev Report](https://juliomoralesb.github.io/user-management-api-challenge/report-dev.html)
  - [Prod Report](https://juliomoralesb.github.io/user-management-api-challenge/report-prod.html)
- **Check Annotations** — The workflow publishes inline test results via `dorny/test-reporter`, visible in the **Checks** tab of any PR or push.
- **Artifacts** — JUnit XML and HTML reports can also be downloaded from the workflow run's **Artifacts** section.

## Bug Report

All discovered bugs and spec mismatches are documented in [BUGS.md](BUGS.md).
