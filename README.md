# Log Unit  
Simple RestAPI service/unit for ecosystem where all logs from other services are stored and accessible in one place.
## Downloading
```bash
git clone https://github.com/denver-code/logunit
cd logunit
```
## Activating Shell
```bash
poetry shell
```
## Installation
> **Note:** This project uses [Poetry](https://python-poetry.org/) for dependency management.
```bash
poetry install
```
Rename `sample.env` to `.env` and fill it with your data.
## Generating Keys for Encryption
```bash
python3 genrsa.py
```
This will generate `private.pem` and `public.pem` files in the root directory of the project. Store `private.pem` in a safe as it is used for decryption.  
If you will lose private key, you will lose all your logs without ability to restore them.
## Running
```bash
poetry run uvicorn app.main:app
```
## Docker
```bash
docker-compose up --build -d
```

## Api documentation
Api documentation is available at `/docs` endpoint.
But [here](API.md) is some examples.
