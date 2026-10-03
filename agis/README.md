# AgisRecon2

**AgisRecon2** is a modular command-line reconnaissance framework designed for authorized cybersecurity reconnaissance and security assessment.

## Features

* Modular reconnaissance architecture
* Centralized configuration
* External tool execution
* Input validation
* Logging and error handling
* Terminal output
* JSON report generation
* Markdown report generation
* Workspace for scan data
* Module availability detection
* Clean project structure

## Project Structure

```text
AgisRecon2/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── tools.py
│   └── constants.py
│
├── modules/
│   ├── __init__.py
│   ├── base.py
│   ├── manager.py
│   ├── subfinder.py
│   ├── assetfinder.py
│   ├── dnsx.py
│   ├── httpx.py
│   ├── nmap.py
│   ├── waybackurls.py
│   ├── katana.py
│   └── nuclei.py
│
├── utils/
│   ├── __init__.py
│   ├── runner.py
│   ├── parser.py
│   ├── logger.py
│   ├── validator.py
│   ├── file_manager.py
│   ├── banner.py
│   ├── colors.py
│   └── helpers.py
│
├── output/
│   ├── __init__.py
│   ├── terminal.py
│   ├── json.py
│   ├── markdown.py
│   └── report.py
│
├── workspace/
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

* Python 3
* Required Python packages listed in `requirements.txt`
* Reconnaissance tools used by the selected modules

Current Python dependency:

```text
colorama>=0.4.6
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd AgisRecon2
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

### Linux

```bash
source .venv/bin/activate
```

Install Python dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Usage

Show the application help:

```bash
python3 main.py --help
```

Show the AgisRecon2 version:

```bash
python3 main.py --version
```

List available modules:

```bash
python3 main.py --list-modules
```

Run a module:

```bash
python3 main.py --target example.com --module subfinder
```

Generate JSON output:

```bash
python3 main.py --target example.com --module subfinder --output json
```

Generate Markdown output:

```bash
python3 main.py --target example.com --module subfinder --output markdown
```

Generate all supported outputs:

```bash
python3 main.py --target example.com --module subfinder --output all
```

## Output

Generated reports are stored under:

```text
output/
├── json/
└── markdown/
```

Runtime reconnaissance data can be stored in:

```text
workspace/
```

Application logs are stored in:

```text
logs/
```

The `logs/`, generated output, and runtime workspace data are ignored by Git.

## Available Modules

AgisRecon2 currently supports the following modules:

| Module        | Purpose                         |
| ------------- | ------------------------------- |
| `subfinder`   | Passive subdomain enumeration   |
| `assetfinder` | Domain and subdomain discovery  |
| `dnsx`        | DNS resolution and probing      |
| `httpx`       | HTTP service probing            |
| `nmap`        | Network/service scanning        |
| `waybackurls` | Historical URL discovery        |
| `katana`      | Web crawling                    |
| `nuclei`      | Vulnerability template scanning |

A module can only execute when its required external tool is installed and available on the system.

Check module availability with:

```bash
python3 main.py --list-modules
```

## Architecture

The framework follows a layered structure:

```text
main.py
   │
   ├── config/
   │
   ├── modules/
   │
   ├── utils/
   │
   └── output/
```

### `config/`

Contains application settings, tool definitions, and constants.

### `modules/`

Contains the reconnaissance modules and module manager.

### `utils/`

Contains reusable utilities such as:

* command execution
* parsing
* logging
* validation
* file management
* terminal colors
* helper functions

### `output/`

Handles presentation and report generation:

* Terminal
* JSON
* Markdown

### `workspace/`

Used for runtime reconnaissance data and working files.

## Testing

Basic framework checks:

```bash
python3 main.py --version
```

```bash
python3 main.py --list-modules
```

Test a reconnaissance module against an authorized target:

```bash
python3 main.py --target example.com --module subfinder
```

Test JSON generation:

```bash
python3 main.py --target example.com --module subfinder --output json
```

Test Markdown generation:

```bash
python3 main.py --target example.com --module subfinder --output markdown
```

## Error Handling

AgisRecon2 validates input and handles common execution failures, including:

* Invalid targets
* Missing modules
* Unavailable external tools
* Command execution failures
* Command timeouts
* Invalid output formats
* File and directory errors

Errors should be reported cleanly without exposing unnecessary Python tracebacks to normal CLI users.

## Legal and Ethical Use

AgisRecon2 is intended for **authorized security testing, cybersecurity education, research, and reconnaissance of systems you have permission to assess**.

Do not use this framework against systems, networks, domains, or applications without appropriate authorization.

The user is responsible for complying with all applicable laws, regulations, and engagement rules.

## Version

```text
AgisRecon2 v1.0.0
```

## License

MIT License
