# Go Driver Service



## Data Migration - Goose

```bash
cd sql/schema
goose postgres postgres://<db_user>:<db_password>@localhost:5432/<db_name> up
```

## Update Database Handlers
```bash
sqlc generate
```

## Update swagger

```bash
swag init -o './api' -g './cmd/main.go' --parseDependency
swag fmt
```

> Visit: `http://0.0.0.0:3000/swagger/index.html`