


# Run Containers

```
docker compose up -d
```

# Link to Swagger UI

http://localhost:8000/docs#/


# Superset Kurulumu
```shell
docker exec -it superset sh
```
yaptıktan sonra

```bash
superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@localhost \
              --password secret


superset db upgrade

superset init
```