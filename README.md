# Codacy Basic Coding Standard Generator

This script creates a basic coding standard in Codacy that enables specific languages and tools while disabling minor findings. This ensures a focus on impactful code quality issues.

## Prerequisites

- Python 3.8 or higher
- Codacy API token
- Codacy organization name

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd basic-coding-standard
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Create a `.env` file in the project root or set the following environment variables:

```bash
CODACY_API_TOKEN=your_api_token_here
CODACY_ORG_NAME=your_organization_name
CODACY_PROVIDER=gh  # For GitHub, adjust for your provider
CODACY_API_URL=https://app.codacy.com  # Optional, defaults to this value
LOG_LEVEL=INFO  # Optional, defaults to INFO
```

## Supported Languages

The following languages are enabled in the coding standard:

- Web Technologies: HTML, CSS, JavaScript, TypeScript, SASS, LESS
- Backend Languages: Python, Java, C, C++, C#, Go, Ruby, PHP, Kotlin, Scala
- Shell Scripting: Shell, PowerShell
- Mobile Development: Swift, Objective C, Dart
- Configuration & Markup: JSON, YAML, XML, Markdown
- Infrastructure: Dockerfile, Terraform
- Other Languages: CoffeeScript, JSP, Perl, Lua, Groovy, Lisp, Visual Basic, Visual Force, Velocity

## Usage

Run the script from the project root directory:

```bash
# Make sure you're in the project root directory
python -m src.main create --project-name "My Coding Standard"
```

### Command Line Options

- `--project-name`: Name for the new coding standard (required)
- `--dry-run`: Preview changes without applying them
- `--verbose`: Increase logging detail
- `--output`: Specify custom log file location (default: logs/codacy_standard_YYYY-MM-DD.log)

### Example

```bash
# Basic usage
python -m src.main create --project-name "Enterprise Standard"

# With verbose logging and custom output
python -m src.main create --project-name "Enterprise Standard" --verbose --output "./custom_log.log"

# Dry run to preview changes
python -m src.main create --project-name "Enterprise Standard" --dry-run
```

## Logging

The script creates detailed logs of all operations, including:
- Enabled languages and tools
- Disabled minor findings
- API interactions
- Errors and warnings

Logs are stored in the `logs` directory by default, with filenames following the pattern: `codacy_standard_YYYY-MM-DD.log`

## Error Handling

The script includes comprehensive error handling for:
- Missing/invalid environment variables
- API connection failures
- Rate limiting
- Permission issues
- Invalid responses

Each error is logged with detailed information to help troubleshoot issues.
