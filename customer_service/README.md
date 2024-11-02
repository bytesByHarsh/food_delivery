## Customer Backend Solution

## Installation

### Requirements
- `Python 3.10`
- PostgreSQL

Create a database and give user access. Make sure you enter the same details in `.env` file.

`.env.example` file is already created for reference.

```bash
sudo snap install ruff
pip install -r requirements.txt
alembic upgrade head
```

## Run Application

```bash
#After Starting virtualenv

python app/main.py
```

## Alembic

### Generate new alembic version
```bash
alembic revision --autogenerate -m "Init Migration"
```

### Upgrade

```bash
alembic upgrade head
```

### Downgrade

```bash
alembic downgrade
```