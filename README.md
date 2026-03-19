# Scalable Backend with Automated CI/CD and Infrastructure as Code


## Description

This project demonstrates the design of a backend system with a complete DevOps pipeline, 
including CI/CD automation, containerization and infrastructure provisioning using Ansible.

## Technologies

- python (FastAPI)
- Docker
- GitHub Actions
- Ansible
- PyTest

## Architecture

...

## CI / CD Pipeline

On each push, GitHub Actions triggers a pipeline including _linting_, _testing_ and _build_ stages.
Pull requests trigger environment-specific workflows (development, staging, production).
After merge, the pipeline automatically deploys the updated version.

## Infrastructure

Infrastructure provisioning and environment setup are automated using Ansible playbooks, 
ensuring consistency across environments.

## How to Play

1. Create a GitHub Issue.
2. Assign issue to me.
3. On GitHub Issue Page: create branch (feature/bugfix/release/docs/hotfix).
4. Implement changes on new branch.
5. Commit and create PR.
6. Review PR.
7. Merge on `develop` branch.

