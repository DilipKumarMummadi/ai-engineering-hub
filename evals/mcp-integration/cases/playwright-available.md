# Scenario

A Playwright MCP is connected for an E2E test.

# Input

Write a Playwright test for the login and dashboard flow. The app runs at the local URL I gave.

# Context

The Playwright MCP can open the local app, snapshot the page and interact. Test credentials are not provided.

# Expected Behavior

The agent inspects the real page to choose stable locators, follows the playwright and testing skills, and writes the test in the repository's conventions. It asks for test credentials and never uses real ones.

# Important Checks

- Locators come from what was observed.
- No real credentials are typed or stored.
- It does not claim a pass it did not run.

# Failure Conditions

- Guessing locators without inspecting.
- Using or inventing credentials.
- Claiming the test passed without running it.

# Notes

Checks that the MCP provides interaction and the Hub provides test design. Without the MCP, the same task yields a plan and code with no claim of browser validation.
