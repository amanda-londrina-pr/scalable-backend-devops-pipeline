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

## How to Run

[Click here and verify how to run this project.](/docs/how_to_run.md)

## How to Play

[Click here and verify the process of develop](/docs/how_to_play.md)

## About Python Tools

[Click here and read about the python tools](/docs/python_tools.md)

