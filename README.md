


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



terminalde "tree" yazarsak proje directorysini yazdırır. "tree ls" daha detaylı olanı.



## Portların Çakışması

Bazen farklı uygulamalar aynı portlarda çakıştığı için veritabanına bağlantı kurulamaz. (Örn: MCP, Jupyter Notebook) Bu durumda aşağıdaki komut ile portun kullanılıp kullanılmadığı kontrol edilebilir.

```sh
netstat -ano | findstr 5432
```