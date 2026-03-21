# Scalable Backend with Automated CI/CD and Infrastructure as Code

## Description

This project demonstrates the design of a backend application using FastAPI, combined with DevOps practices
such as CI/CD automation, containerization and infrastructure provisioning using Ansible.

## Technologies

- python (FastAPI)
- Docker
- GitHub Actions
- Ansible
- PyTest

## 🏗️ Architecture Overview

This project follows a layered architecture approach, separating concerns between domain logic, infrastructure, and API
interface. This improves maintainability, testability, and scalability.

### Domain Layer (Business Rules)

The domain layer contains the core business logic and rules of the application.

* Example: `TaskStatus` enum
* Defines valid states for a task (e.g., `PENDING`, `IN_PROGRESS`, `DONE`)
* Prevents invalid state transitions and enforces consistency

This layer is independent of frameworks and external libraries.

---

### Infrastructure Layer (Persistence)

The infrastructure layer is responsible for data persistence and database interaction.

* Example: `task_model.py` (Tortoise ORM model)
* Maps domain entities to database tables
* Handles low-level concerns such as schema definition and queries

---

### Interface Layer (API / Schemas)

The interface layer defines how the application communicates with the outside world.

* Example: `task_schema.py` (Pydantic schemas)
* Handles request validation and response serialization
* Ensures data integrity at the API boundary

---

### Why this separation?

* Clear separation of concerns
* Easier to maintain and extend
* Better alignment with real-world backend architecture
* Prepares the codebase for scaling and more complex business rules

## CI / CD Pipeline

On each push, GitHub Actions triggers a pipeline including _linting_, _testing_ and _build_ stages.
Pull requests trigger environment-specific workflows (development, staging, production).
After merge, the pipeline automatically deploys the updated version.

## Infrastructure

Infrastructure provisioning and environment setup are automated using Ansible playbooks,
ensuring consistency across environments.

## How to Run

[Click here and verify how to run this project.](/docs/how_to_run.md)

## How to Play

[Click here and verify the process of develop](/docs/how_to_play.md)

## About Python Tools

[Click here and read about the python tools](/docs/python_tools.md)

