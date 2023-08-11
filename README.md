# Log Unit  
Simple RestAPI service/unit for ecosystem where all logs from other services are stored and accessible in one place.

Service not encrypts logs, and does not require authorisation so it's not recommended to use it in production yet, but will be in future.
## Installation
> **Note:** This project uses [Poetry](https://python-poetry.org/) for dependency management.
```bash
git clone https://github.com/denver-code/logunit
cd logunit
poetry install
poetry run uvicorn app.main:app
```
## Docker
```bash
docker-compose up --build -d
```

## Api documentation
Api documentation is available at `/docs` endpoint.
But [here](API.md) is some examples.