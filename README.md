# Library Management System

A web-based application for managing library books, developed using Flask and SQLite.

## Features
- Add new books
- View available books
- Search books by title
- Update book details
- Delete books
- Monitor application metrics

## Technologies Used
- Python
- Flask
- SQLite
- Pytest
- Git and GitHub
- GitHub Actions
- Docker and Docker Compose
- Prometheus and Grafana

## Run Locally

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the application:

```bash
python app.py
```

Open http://localhost:5000 in your browser.

## Run Automated Tests

```bash
python -m pytest -v
```

## Monitoring
- Application: http://localhost:5000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## Deployment
The application can be containerized using Docker and deployed with Docker Compose alongside Prometheus and Grafana.
