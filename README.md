# API Gateway Platform

A Python-based microservices demo with a FastAPI API Gateway, Redis-backed caching and rate limiting, JWT auth, and service registry routing.

## Overview

This project demonstrates a simple API gateway architecture with:
- A FastAPI gateway that routes requests to backend microservices
- JWT authentication and role-based access control (RBAC)
- Redis-based rate limiting and response caching
- A local frontend for testing service calls
- Docker Compose orchestration for the full stack

## Architecture

The gateway is the single entry point for all client requests. It performs:
- Authentication via JWT token validation
- Authorization using user role checks
- Dynamic routing using `registry/registry.json`
- Request logging via middleware
- Prometheus-style metrics exposure on `/metrics`

Backend services are independent microservices in `services/`:
- `user-service`
- `product-service`
- `order-service`

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. Start the stack:

```bash
docker-compose up --build
```

2. Open the frontend in a browser:

```text
http://localhost:8080
```

3. Generate a token:

```bash
curl -X POST "http://localhost:8000/generate-token?role=user"
```

4. Call a backend service through the gateway:

```bash
curl -H "Authorization: Bearer <YOUR_TOKEN>" "http://localhost:8000/user-service/users"
```
