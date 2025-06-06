# PostgreSQL  `match` Tablosu Veri Tipi Güncelleme

## Sorun

Veritabanına `INSERT` işlemi sırasında bazı kolonlara `NaN` (Not a Number) değerleri atanmak istendiğinde, bu değerlerin `integer` veri tipinde tanımlı alanlara yazılamadığı tespit edilmiştir.

### Hata Detayı

Aşağıdaki SQL sorgusu çalıştırılırken hata alınmıştır:

```sql
INSERT INTO match (
    match_id, tournament_id, season_id, round, 
    start_timestamp, status_code, status_type, winner_code,
    home_team_name, home_team_id, away_team_name, away_team_id,
    home_score_period1, home_score_period2, home_score_normaltime,
    away_score_period1, away_score_period2, away_score_normaltime,
    time_injury_time1, time_injury_time2
) VALUES (
    %(match_id)s, %(tournament_id)s, %(season_id)s, %(round)s, 
    %(start_timestamp)s, %(status_code)s, %(status_type)s, %(winner_code)s, 
    %(home_team_name)s, %(home_team_id)s, %(away_team_name)s, %(away_team_id)s, 
    %(home_score_period1)s, %(home_score_period2)s, %(home_score_normaltime)s,
    %(away_score_period1)s, %(away_score_period2)s, %(away_score_normaltime)s,
    %(time_injury_time1)s, %(time_injury_time2)s
) ON CONFLICT (match_id) DO NOTHING;
```

Insert edilmek istenen veri:

```json
{
    "match_id": 12528204,
    "tournament_id": 62,
    "season_id": 63814,
    "round": 3,
    "start_timestamp": 1724695200,
    "status_code": 60,
    "status_type": "postponed",
    "winner_code": NaN,
    "home_team_name": "Trabzonspor",
    "home_team_id": 3051,
    "away_team_name": "Kayserispor",
    "away_team_id": 3072,
    "home_score_period1": NaN,
    "home_score_period2": NaN,
    "home_score_normaltime": NaN,
    "away_score_period1": NaN,
    "away_score_period2": NaN,
    "away_score_normaltime": NaN,
    "time_injury_time1": NaN,
    "time_injury_time2": NaN
}
```

Hata mesajı:
```
(psycopg2.errors.NumericValueOutOfRange) integer out of range
(Background on this error at: https://sqlalche.me/e/20/9h9h)
```

## Çözüm

Sorun `integer` veri tipinin `NaN` değerlerini desteklememesinden kaynaklanmaktadır. Sorunu çözmek için ilgili kolonların veri tipini `double precision` olarak değiştirdik.

Kolonların veri tipi aşağıdaki SQL komutu ile güncellendi ve devamında yapılan insertion işlemi başarılı oldu.

```sql
ALTER TABLE match
    ALTER COLUMN winner_code TYPE double precision USING winner_code::double precision,
    ALTER COLUMN home_score_period1 TYPE double precision USING home_score_period1::double precision,
    ALTER COLUMN home_score_period2 TYPE double precision USING home_score_period2::double precision,
    ALTER COLUMN home_score_normaltime TYPE double precision USING home_score_normaltime::double precision,
    ALTER COLUMN away_score_period1 TYPE double precision USING away_score_period1::double precision,
    ALTER COLUMN away_score_period2 TYPE double precision USING away_score_period2::double precision,
    ALTER COLUMN away_score_normaltime TYPE double precision USING away_score_normaltime::double precision;
```


## Çoğaltılmış satırlar için çözüm

```sql
DELETE FROM statistic
WHERE ctid NOT IN (
  SELECT MIN(ctid)
  FROM statistic
  GROUP BY match_id, period, group_name, statistics_name, value_type, key, statistics_type, away_value, home_value
);
```

