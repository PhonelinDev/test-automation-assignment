# Test Automation Assignment

## Overview

| Question | Topic | Language / Tool |
|----------|-------|-----------------|
| 1 | Find duplicate items from two lists | Python |
| 2 | Login automation test | Playwright + TypeScript |
| 3 | REST API testing | Playwright + TypeScript |
| 4 | Mobile app testing (Minimal-Todo) | Appium + Python |
| 5 | Jenkins CI/CD pipeline | Groovy |
| 6 | Simple cipher decryption | Python |

---

## Project Structure

```
test-assignment/
├── pages/
│   └── LoginPage.ts          # Page Object for login page
├── question1/
│   └── duplicate.py          # Find duplicates from two lists
├── question4/
│   ├── Minimal-Todo/         # Android app source code
│   ├── test_cases_appium.md  # Test cases documentation
│   └── test_minimal_todo.py  # Appium automation script
├── question5/
│   └── Jenkinsfile           # Jenkins pipeline
├── question6/
│   └── cipher.py             # Simple cipher solution
├── tests/
│   ├── question2/
│   │   └── login.spec.ts     # Login automation tests
│   └── question3/
│       └── api.spec.ts       # REST API tests
└── playwright.config.ts
```

---

## How to Run

### Question 1 — Find Duplicates (Python)
```bash
python question1/duplicate.py
```

### Question 2 & 3 — Playwright Tests (TypeScript)
```bash
npm ci
npx playwright install --with-deps chromium
npx playwright test
```
View HTML report:
```bash
npx playwright show-report playwright-report
```

### Question 4 — Mobile App Tests (Appium + Python)

**Prerequisites:**
- Android Studio + Android Emulator (API 28+)
- Appium server running

```bash
# Install dependencies
pip install appium-python-client pytest
npm install -g appium
appium driver install uiautomator2

# Start Android Emulator from Android Studio

# Start Appium server
appium

# Run tests
pytest question4/test_minimal_todo.py -v
```

### Question 5 — Jenkins Pipeline

Import `question5/Jenkinsfile` into Jenkins.

Pipeline stages:
1. **Checkout Code From Git** — pull source code
2. **Run Test Automate** — install dependencies and run Playwright tests
3. **Send Result To Jenkins** — publish HTML report

### Question 6 — Simple Cipher (Python)
```bash
python question6/cipher.py
```

---

## Tools & Technologies

- **Playwright** — Web automation and API testing
- **Appium + UiAutomator2** — Android mobile automation
- **Python** — Scripting and mobile test automation
- **TypeScript** — Web automation scripts
- **Jenkins** — CI/CD pipeline
