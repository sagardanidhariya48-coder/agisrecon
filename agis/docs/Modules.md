# Modules

## Overview

AgisRecon is built using a modular architecture where each module is responsible for a single reconnaissance task. Modules are independent, reusable, and communicate through structured data. This design simplifies development, testing, and future expansion.

---

# Module Overview

```text
CLI
 │
 ▼
Controller
 │
 ├── Config Module
 ├── Logging Module
 ├── Asset Discovery Module
 ├── DNS Enumeration Module
 ├── HTTP Probe Module
 ├── Port Scanner Module
 ├── Service Detection Module
 ├── Technology Detection Module
 ├── Vulnerability Scanner Module
 ├── Result Processor Module
 └── Output Module
```

---

# Core Modules

## Configuration Module

### Purpose

Loads application settings before execution.

### Responsibilities

* Load configuration files
* Read environment variables
* Validate settings
* Provide global configuration

---

## Logging Module

### Purpose

Records application activity.

### Responsibilities

* Execution logs
* Error logs
* Debug logs
* Scan summaries

---

## Asset Discovery Module

### Purpose

Discovers assets associated with the target.

### Responsibilities

* Subdomain discovery
* Passive reconnaissance
* Asset collection

### Output

* Asset list

---

## DNS Enumeration Module

### Purpose

Collects DNS information for discovered assets.

### Responsibilities

* DNS record lookup
* Record validation
* DNS resolution

### Output

* DNS records

---

## HTTP Probe Module

### Purpose

Identifies live web services.

### Responsibilities

* Check HTTP/HTTPS availability
* Collect status codes
* Retrieve titles
* Detect redirects

### Output

* Live hosts

---

## Port Scanner Module

### Purpose

Discovers open network ports.

### Responsibilities

* TCP scanning
* UDP scanning
* Port validation

### Output

* Open ports

---

## Service Detection Module

### Purpose

Identifies services running on discovered ports.

### Responsibilities

* Detect service names
* Detect service versions
* Banner collection

### Output

* Service information

---

## Technology Detection Module

### Purpose

Detects technologies used by web applications.

### Responsibilities

* Web server detection
* Framework detection
* CMS detection
* Programming language detection

### Output

* Technology stack

---

## Vulnerability Scanner Module

### Purpose

Performs automated security checks.

### Responsibilities

* Run vulnerability templates
* Collect findings
* Categorize issues

### Output

* Vulnerability report

---

## Result Processor Module

### Purpose

Processes outputs from all modules.

### Responsibilities

* Merge results
* Remove duplicates
* Validate data
* Prepare final dataset

### Output

* Processed results

---

## Output Module

### Purpose

Exports reconnaissance results.

### Responsibilities

* JSON output
* Text output
* HTML report generation

### Output

* Final reports

---

# Module Communication

```text
Configuration
      │
      ▼
Controller
      │
      ▼
Recon Modules
      │
      ▼
Result Processor
      │
      ▼
Output Module
```

---

# Module Design Principles

* Single responsibility
* Independent execution
* Reusable components
* Minimal coupling
* High cohesion
* Configurable behavior
* Easy testing
* Easy extension

---

# Future Modules

Future versions of AgisRecon may include:

* Cloud Asset Discovery
* Screenshot Module
* JavaScript Analysis
* Directory Enumeration
* API Discovery
* Secret Detection
* AI Analysis
* Plugin Manager
* Distributed Scanning
* Report Dashboard
