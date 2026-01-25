# Getting Started

This guide walks you through setting up Pacta in your Python project to enforce architectural rules.

## Prerequisites

- Python 3.10 or later
- A Python project with importable modules

## Installation

Install Pacta from PyPI:

```bash
pip install pacta
```

For chart image export (PNG/SVG), install with visualization support:

```bash
pip install pacta[viz]
```

Verify the installation:

```bash
pacta --help
```

## Step 1: Define Your Architecture

Create an `architecture.yml` file in your project root. This file defines your system structure and architectural layers.

```yaml
version: 1
system:
  id: myapp
  name: My Application

containers:
  backend:
    name: Backend Service
    code:
      roots:
        - src
      layers:
        domain:
          name: Domain Layer
          description: Core business logic
          patterns:
            - src/domain/**
        application:
          name: Application Layer
          description: Use cases and orchestration
          patterns:
            - src/application/**
        infra:
          name: Infrastructure Layer
          description: External services, databases, APIs
          patterns:
            - src/infra/**
```

**Key concepts:**

| Concept | Description |
|---------|-------------|
| `system` | Top-level identifier for your project |
| `containers` | Deployable units (services, apps) |
| `roots` | Directories to scan for code |
| `layers` | Architectural boundaries within a container |
| `patterns` | Glob patterns mapping code to layers |

## Step 2: Define Your Rules

Create a `rules.pacta.yml` file to define architectural constraints:

```yaml
# Domain layer must not depend on Infrastructure
rule:
  id: no_domain_to_infra
  name: Domain cannot depend on Infrastructure
  severity: error
  target: dependency
  when:
    all:
      - from.layer == domain
      - to.layer == infra
  action: forbid
  message: Domain layer must not import from Infrastructure
  suggestion: Use dependency injection and define interfaces in the domain layer

# Domain layer must not depend on Application
rule:
  id: no_domain_to_application
  name: Domain cannot depend on Application
  severity: error
  target: dependency
  when:
    all:
      - from.layer == domain
      - to.layer == application
  action: forbid
  message: Domain layer must be independent of use cases
```

**Rule structure:**

| Field | Description |
|-------|-------------|
| `id` | Unique identifier for the rule |
| `name` | Human-readable rule name |
| `severity` | `error` (fails build), `warning`, or `info` |
| `target` | What to evaluate (`dependency` or `node`) |
| `when` | Conditions that trigger the rule |
| `action` | `forbid`, `allow`, or `require` |
| `message` | Explanation shown on violation |
| `suggestion` | How to fix the violation |

## Step 3: Run Your First Scan

Scan your project:

```bash
pacta scan . --model architecture.yml --rules rules.pacta.yml
```

**Example output with violations:**

```
✗ 2 violations (2 error)

  ✗ ERROR [no_domain_to_infra] Domain cannot depend on Infrastructure @ src/domain/user.py:3:1
    status: new
    "myapp.domain.UserService" in domain layer imports "myapp.infra.Database" in infra layer

  ✗ ERROR [no_domain_to_application] Domain cannot depend on Application @ src/domain/order.py:5:1
    status: new
    "myapp.domain.OrderEntity" in domain layer imports "myapp.application.OrderService" in application layer
```

**Example output with no violations:**

```
✓ 0 violations
```

## Step 4: Set Up Baseline (Optional)

If you have existing violations you can't fix immediately, create a baseline. Future scans will only fail on *new* violations:

```bash
# Save current state as baseline
pacta scan . --model architecture.yml --rules rules.pacta.yml --save-ref baseline

# Later scans compare against baseline
pacta scan . --model architecture.yml --rules rules.pacta.yml --baseline baseline
```

With a baseline, output shows violation status:

```
✗ 3 violations (2 error, 1 warning) [1 new, 2 existing]

  ✗ ERROR [no_domain_to_infra] Domain cannot depend on Infrastructure @ src/domain/new_feature.py:3:1
    status: new        <-- This is new, will fail CI

  ✗ ERROR [no_domain_to_infra] Domain cannot depend on Infrastructure @ src/domain/legacy.py:10:1
    status: existing   <-- Known issue, won't fail CI
```

## Step 5: Track History

Every scan creates a content-addressed snapshot. View your architecture evolution:

```bash
# View timeline of snapshots
pacta history show . --last 10

# View violation trends over time
pacta history trends . --metric violations

# Export chart as image
pacta history trends . --output violations.png
```

## Project Structure Example

Here's a typical project structure with Pacta configuration:

```
myproject/
├── architecture.yml      # Architecture definition
├── rules.pacta.yml       # Architectural rules
├── src/
│   ├── domain/           # Business logic (no external dependencies)
│   │   ├── __init__.py
│   │   ├── entities.py
│   │   └── services.py
│   ├── application/      # Use cases (orchestrates domain + infra)
│   │   ├── __init__.py
│   │   └── use_cases.py
│   └── infra/            # External services (implements domain interfaces)
│       ├── __init__.py
│       ├── database.py
│       └── api_client.py
└── .pacta/               # Pacta data directory (auto-created)
    └── snapshots/        # Content-addressed snapshot storage
```

## Next Steps

- [CLI Reference](cli.md) - All commands and options
- [Architecture Model](architecture.md) - Full configuration schema
- [Rules DSL](rules.md) - Advanced rule conditions
- [CI Integration](ci-integration.md) - GitHub Actions and GitLab CI setup
