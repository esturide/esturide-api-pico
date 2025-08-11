# Esturide (p) API

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![FireBase](https://img.shields.io/badge/firebase-ffca28?style=for-the-badge&logo=firebase&logoColor=black)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

The Esturide API, built using the modern, fast (high-performance) FastAPI framework, is designed to provide robust backend functionality for the Esturide platform.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Docker Commands](#docker-commands)
- [Contributing](#contributing)

## Introduction

This project encapsulates the backend service of Esturide, offering high scalability, speed, and ease of use. FastAPI's elegant design and Docker's containerization ensure a seamless development and deployment experience.

## Installation

Ensure you have the latest versions of [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your system to work with containerization.

### Initial Setup

1. **Clone the Repository**:
```
git clone https://github.com/esturide/esturide-api-pico.git
cd esturide-api-pico
```

2. **Install Docker**:
- Follow the instructions at [Docker's website](https://www.docker.com/get-started) to install Docker.

### To Run the Application

Execute the following command in the terminal:
```
docker compose up --build
```

This command will build the Docker image if it doesn't exist and start the service.

## Usage

Once the application is running, visit the `/docs` endpoint (e.g., http://localhost:8000/docs) to view the Swagger UI documentation, which provides a detailed explanation of each endpoint and the ability to test them directly.

## Docker Commands

- `docker compose up`: Starts the containers. If the image does not exist, Docker Compose automatically builds it using the `Dockerfile`.
- `docker compose up --build`: Forces the build of the image even if it already exists and then starts the container. Useful when you have made changes to the `Dockerfile` or need to rebuild the image for any other reason.
- `docker system prune -a --volumes`: Force and purge data base.

## Contributing

Contributions are what make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

### Setting Up Your Development Environment

Before you start contributing, it's important to set up your development environment. This includes installing necessary tools and configuring pre-commit hooks to ensure code quality.