# Inventory Management CLI

A production-oriented, ledger-based inventory management system 
implemented as a Python command-line application.

This project is designed to demonstrate clean architecture, strong 
domain modeling, and real-world data integrity practices using PostgreSQL.
Rather than mutating stock counts directly, all inventory changes are recorded
as immutable stock movement events, providing a complete audit trail and
deterministic state reconstruction.

---

## Key Concepts

### Ledger-based inventory
Inventory quantities are **derived**, not stored. Every increase or decrease in
stock is recorded as a movement event (receive, issue, adjust). Current on-hand
inventory is calculated from this ledger, ensuring traceability and auditability.

### Clear separation of concerns

The system is structured into distinct layers:

* CLI layer - argument parsing and output formatting
* Application layer - use cases and orchestration
* Domain layer - business rules and invariants
* Infrastructure layer - database, persistence, and exports

This makes the core logic reusable and easy to adapt into other interfaces (e.g., REST APIs)
without rewrites.

---

## Features

* Item catalog management (SKU-based)
* Ledger-based stock tracking
* Stock receiving, issuing, and adjustment operations
* Low-stock and inventory summary reports
* PostgreSQL persistence with transactional guarantees
* Database migrations via Alembic
* Rich, readable CLI output
* Script-friendly JSON output mode
* Docker-based local development setup

---

## Command Overview

```bash
inv item add
inv item update
inv item list
inv item deactivate

inv stock receive
inv stock issue
inv stock adjust
inv stock on-hand

inv report inventory
inv report low-stock

inv db upgrade
ing db status
```
Each command is explicitly modeled, validated, and auditable. Item catalog 
operations never directly affect inventory quantities.

---

## Example Usage
```bash
inv item add \
  --sku WIDGET-001 \
  --name "Standard Widget" \
  --unit each \
  --reorder-threshold 10
  
inv stock receive \
  --sku WIDGET-001 \
  --quantity 50 \
  --reason "Initial stock"
  
inv report low-stock
```

---

## Technology Stack
* Python 3.12+
* Typer (CLI framework)
* Rich (terminal output)
* PostgreSQL
* SQLModel / SQL Alchemy 2x
* Alembic (migrations)
* pytest, ruff
* Docker & Docker Compose

---

## Design Goals
* Favor correctness and auditability over convenience
* Make invariants explicit and enforceable
* Keep side effects isolated
* Support automation and scripting
* Be readable and reviewable by other engineers

---

## Future Extensions
* Multi-location inventory
* Reservation / hold system
* Inventory valuation reports
* REST or GraphQL API adapter
* Role-based access control

---

## License
Apache License

---