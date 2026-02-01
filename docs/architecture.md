# Architecture Model

The architecture model defines your system structure in YAML.

Pacta supports two schema versions:

- **v1** — Flat containers with layers. Simple and sufficient for single-service architectures.
- **v2** — Nested containers with `kind` and `contains`. Designed for microservices and modular monoliths.

The loader auto-detects the version from the `version:` key. If absent, v1 is assumed.

---

## v1 Schema

### File Format

Create `architecture.yml` in your repository root:

```yaml
version: 1

system:
  id: my-system
  name: My System

containers:
  my-app:
    name: My Application
    description: Main application container
    code:
      roots:
        - src
      layers:
        ui:
          name: UI Layer
          patterns:
            - src/ui/**
        application:
          name: Application Layer
          patterns:
            - src/application/**
        domain:
          name: Domain Layer
          patterns:
            - src/domain/**
        infra:
          name: Infrastructure Layer
          patterns:
            - src/infra/**

contexts: {}
```

### Schema Reference (v1)

#### system

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique system identifier |
| `name` | string | Yes | Human-readable name |

#### containers

Map of container definitions.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Container name |
| `description` | string | No | Container description |
| `context` | string | No | Bounded context reference |
| `code` | object | No | Code mapping configuration |
| `tags` | list | No | Tags inherited by nodes in this container |

#### code

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `roots` | list | Yes | Source root directories |
| `layers` | map | No | Layer definitions |

#### layers

Map of layer definitions.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | No | Layer display name |
| `description` | string | No | Layer description |
| `patterns` | list | Yes | Glob patterns matching layer files |

#### relations

```yaml
relations:
  - from: container-a
    to: container-b
    protocol: http
    description: A calls B
```

### Example: Clean Architecture (v1)

```yaml
version: 1

system:
  id: healthcare-scheduling
  name: Healthcare Scheduling

containers:
  scheduling-api:
    name: Scheduling API
    context: scheduling
    code:
      roots:
        - services/scheduling-api
      layers:
        ui:
          name: Presentation
          patterns:
            - services/scheduling-api/api/**
        application:
          name: Use Cases
          patterns:
            - services/scheduling-api/app/**
        domain:
          name: Domain
          patterns:
            - services/scheduling-api/domain/**
        infra:
          name: Infrastructure
          patterns:
            - services/scheduling-api/infra/**
```

---

## v2 Schema

v2 adds **nested containers**, explicit **container kinds**, and the `interactions:` alias for relations. v1 files remain fully valid — no migration is required.

### What's New in v2

| Feature | Description |
|---------|-------------|
| `kind` | Required on every container: `service`, `module`, or `library` |
| `contains` | Nest child containers inside a parent |
| `interactions` | Alias for `relations` (both accepted) |
| Dot-qualified IDs | Nested containers get IDs like `billing-service.invoice-module` |
| Context inheritance | Children inherit parent's `context` unless they override it |

### File Format (v2)

```yaml
version: 2

system:
  id: my-platform
  name: My Platform

contexts:
  billing:
    name: Billing Context

containers:
  billing-service:
    kind: service
    name: Billing Service
    context: billing
    code:
      roots: [services/billing]
      layers:
        api: [services/billing/api/**]
        domain: [services/billing/domain/**]
    contains:
      invoice-module:
        kind: module
        name: Invoice Module
        code:
          roots: [services/billing/domain/invoice]
          layers:
            model: [services/billing/domain/invoice/model/**]
            repo: [services/billing/domain/invoice/repo/**]

  shared-utils:
    kind: library
    name: Shared Utilities
    code:
      roots: [libs/shared]

interactions:
  - from: billing-service
    to: shared-utils
    protocol: import
```

### Schema Reference (v2)

v2 containers extend the v1 schema with these additional fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `kind` | string | **Yes** | `service`, `module`, or `library` |
| `contains` | map | No | Nested child containers (same schema, recursive) |

All v1 container fields (`name`, `description`, `context`, `code`, `tags`) remain unchanged.

### Container Kinds

| Kind | Meaning |
|------|---------|
| `service` | Deployable service or application |
| `module` | Logical module within a service |
| `library` | Shared library used by other containers |

### Dot-Qualified IDs

Nested containers are addressed using dot-qualified IDs. For the example above:

- `billing-service` — the top-level service
- `billing-service.invoice-module` — the nested module

These IDs are used in `interactions`, rules, and enrichment output.

### Context Inheritance

Children inherit their parent's `context:` unless they explicitly set their own:

```yaml
containers:
  billing-service:
    kind: service
    context: billing          # set here
    contains:
      invoice-module:
        kind: module          # inherits context: billing
      payments-module:
        kind: module
        context: payments     # overrides with own context
```

### Version Detection

| `version:` value | Behavior |
|------------------|----------|
| absent | v1 (default) |
| `1` | v1 |
| `2` | v2 — `kind` required, `contains` and `interactions` supported |
| anything else | Error |

### v1 → v2 Key Mapping

| v1 key | v2 key | Notes |
|--------|--------|-------|
| `context:` | `context:` | Unchanged |
| `relations:` | `interactions:` | Both accepted in v2; `relations:` takes precedence if both present |
| _(n/a)_ | `contains:` | New in v2 |
| _(n/a)_ | `kind:` | Required in v2 |
