# Rules DSL

Define architectural rules in `rules.pacta.yml`.

## Rule Structure

```yaml
rule:
  id: rule-id
  name: Rule Name
  description: What this rule enforces
  severity: error | warning | info
  target: dependency
  when:
    all:
      - condition1
      - condition2
  action: forbid | allow | require
  message: Violation message
  suggestion: How to fix
```

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique rule identifier |
| `name` | string | Yes | Human-readable name |
| `description` | string | No | Detailed description |
| `severity` | string | Yes | `error`, `warning`, or `info` |
| `target` | string | Yes | What to evaluate (e.g., `dependency`) |
| `when` | object | Yes | Conditions for the rule |
| `action` | string | Yes | `forbid`, `allow`, or `require` |
| `message` | string | No | Message shown on violation (auto-generated if omitted) |
| `suggestion` | string | No | Remediation guidance |

## Available Fields

### Node Fields (`target: node`)

| Field | Description |
|-------|-------------|
| `node.symbol_kind` | Symbol type: `file`, `module`, `class`, `function`, etc. |
| `node.kind` | Container kind: `service`, `module`, `library` (v2 only) |
| `node.service` | Top-level container ancestor (v2 only) |
| `node.path` | File path |
| `node.name` | Symbol name |
| `node.layer` | Architectural layer |
| `node.context` | Bounded context |
| `node.container` | Container ID (dot-qualified for nested containers in v2) |
| `node.tags` | Tags inherited from container |
| `node.fqname` | Fully qualified name |
| `node.language` | Source language |

### Dependency Fields (`target: dependency`)

| Field | Description |
|-------|-------------|
| `from.layer` / `to.layer` | Source/target layer |
| `from.context` / `to.context` | Source/target bounded context |
| `from.container` / `to.container` | Source/target container ID |
| `from.service` / `to.service` | Source/target top-level service (v2 only) |
| `from.kind` / `to.kind` | Source/target container kind (v2 only) |
| `from.fqname` / `to.fqname` | Fully qualified names |
| `from.id` / `to.id` | Full canonical ID strings |
| `dep.type` | Dependency type (`import`, `call`, etc.) |
| `loc.file` | Source location file |

## Conditions

### Layer Conditions

```yaml
from.layer == domain    # Source is domain layer
to.layer == infra       # Target is infra layer
```

### Combining Conditions

```yaml
# All conditions must match
when:
  all:
    - from.layer == domain
    - to.layer == infra

# Any condition can match
when:
  any:
    - to.layer == domain
    - to.layer == application
```

## Example: Clean Architecture Rules (v1)

```yaml
# Domain cannot depend on Infrastructure
rule:
  id: no_domain_to_infra
  name: Domain must not depend on Infrastructure
  description: |
    The domain layer contains pure business logic and should not
    depend on technical implementation details.
  severity: error
  target: dependency
  when:
    all:
      - from.layer == domain
      - to.layer == infra
  action: forbid
  message: Domain layer must not depend on Infrastructure layer
  suggestion: Use dependency injection and define interfaces in the domain layer

# Domain cannot depend on Application
rule:
  id: no_domain_to_application
  name: Domain must not depend on Application
  severity: error
  target: dependency
  when:
    all:
      - from.layer == domain
      - to.layer == application
  action: forbid
  message: Domain layer must not depend on Application layer
  suggestion: Move shared logic to the domain layer

# Domain cannot depend on UI
rule:
  id: no_domain_to_ui
  name: Domain must not depend on UI
  severity: error
  target: dependency
  when:
    all:
      - from.layer == domain
      - to.layer == ui
  action: forbid
  message: Domain layer must not depend on UI layer
  suggestion: Keep domain models free from presentation concerns

# UI should not directly access Infrastructure
rule:
  id: no_ui_to_infra
  name: UI should not directly access Infrastructure
  severity: warning
  target: dependency
  when:
    all:
      - from.layer == ui
      - to.layer == infra
  action: forbid
  message: UI layer should not directly depend on Infrastructure layer
  suggestion: Access infrastructure through application services instead
```

## Example: Cross-Service Rules (v2)

These rules use v2-only fields (`from.service`, `to.service`, `from.kind`, `to.kind`):

```yaml
# Forbid cross-service domain dependencies
rule:
  id: no-cross-service-domain-deps
  name: Domain must not depend on other services
  severity: error
  target: dependency
  action: forbid
  when:
    all:
      - from.service != to.service
      - from.layer == domain
  message: Domain code must not depend on another service

# Libraries must not depend on services
rule:
  id: library-no-service-deps
  name: Libraries must be independent of services
  severity: error
  target: dependency
  action: forbid
  when:
    all:
      - from.kind == library
      - to.kind == service
  message: Library code must not import service code
```
