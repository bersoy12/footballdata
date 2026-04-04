


# Run Containers

```
docker compose up -d
```


# Dikkat
Aşağıdaki komut bütün containerları siler.

```
docker compose down
```


# Link to Swagger UI

http://localhost:8000/docs#/

# n8n latest version re-build

```
docker compose up -d --build n8n
```

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


uygulama ilk kez build alındıktan sonra

1. veritabanı şeması yüklenmeli.

docker exec -it postgres bash -> postgres servisinin içerisine girilir.


psql -U postgres -d football -f /scripts/schema_utf8.sql -> bununla football veritabanına bağlanılır ve schema_utf8.sql dosyasına göre tabloları oluşturur.

psql -U postgres -d football -> bu komut girildiğinde football veritabanına bağlanmış olur.

\d yazılarak tablo bilgileri görülebilir.