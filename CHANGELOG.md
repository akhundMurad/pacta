# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.2] - 2025-01-20

### Added

- History tracking with content-addressed snapshot store
- `pacta history show` command to view architecture timeline
- `pacta history export` command for JSON export of history data
- `pacta history trends` command with ASCII charts for visualizing metrics over time
- Optional matplotlib support for PNG/SVG chart export (`pip install pacta[viz]`)
- Human-readable violation explanations in text output
- Expanded contributing guide with project structure and development workflow

### Changed

- License changed to Apache-2.0
- README repositioned to focus on architecture governance

## [0.0.1] - 2025-01-15

### Added

- Initial release
- Python AST analyzer for static code analysis
- Architecture model definition via `architecture.yml`
  - System and container definitions
  - Layer definitions with glob patterns
  - Code mapping configuration
- Rules DSL via `rules.pacta.yml`
  - Layer dependency constraints
  - Severity levels (error, warning, info)
  - Custom messages and suggestions
- `pacta scan` command for architecture validation
- Snapshot support for versioning architecture state
- Baseline mode for incremental adoption (fail only on new violations)
- `pacta snapshot save` and `pacta diff` commands
- Text and JSON output formats
- MkDocs documentation site

[Unreleased]: https://github.com/akhundMurad/pacta/compare/v0.0.2...HEAD
[0.0.2]: https://github.com/akhundMurad/pacta/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/akhundMurad/pacta/releases/tag/v0.0.1
