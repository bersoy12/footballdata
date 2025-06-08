import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import create_engine, MetaData, Table, text, select
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import logging
from pathlib import Path

load_dotenv()

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)


file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
docker_formatter = logging.Formatter('%(levelname)s - %(message)s')

operations_handler = logging.FileHandler(log_dir / 'database_operations.log')
operations_handler.setFormatter(file_formatter)

errors_handler = logging.FileHandler(log_dir / 'database_errors.log')
errors_handler.setFormatter(file_formatter)

docker_handler = logging.StreamHandler()
docker_handler.setFormatter(docker_formatter)

logging.basicConfig(
    level=logging.INFO,
    # format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        operations_handler  # tüm veritabanı işlemleri için log
        , errors_handler    # sadece hatalar için log
        , docker_handler    # print gibi konsola yazar
    ]
)


error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler(log_dir / 'database_errors.log')
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
error_logger.addHandler(error_handler)

engine = create_engine(os.getenv('FOOTBALL_URI'))
conn = engine.connect()


def truncate_table(table_name, conn=conn):
    conn.execute(text("TRUNCATE TABLE {} CASCADE;".format(table_name)))
    conn.commit()


def log_error(error_type: str, error_message: str, table_name: str, row_data: dict, sql_query: str = None):
    """Hata bilgilerini JSON formatında loglar"""
    error_log = {
        'timestamp': datetime.now().isoformat(),
        'error_type': error_type,
        'error_message': str(error_message),
        'table_name': table_name,
        'row_data': row_data,
        'sql_query': sql_query
    }
    
    log_file = log_dir / f'errors_{table_name}.json'
    try:
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(error_log)
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)
            
    except Exception as e:
        error_logger.error(f"Log dosyası yazılırken hata oluştu: {str(e)}")
    
    error_logger.error(f"Veritabanı hatası - Tablo: {table_name}, Hata: {error_message}")

def insert_table(df, table_name, engine = engine, conn = conn, on_conflict_columns: list = [], on_conflict_entire_columns: bool = False):
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=engine)
    
    df = df.where(pd.notnull(df), None)
    df = df.replace({pd.NA: None, pd.NaT: None})
    
    rows = df.to_dict(orient='records')
    
    successful_inserts = 0
    failed_inserts = 0
    
    logging.info(f"Data insertion started for table {table_name}. Total {len(rows)} rows.")
    
    for row in rows:
        try:
            insertion = insert(table).values(row)
            if on_conflict_entire_columns:
                insertion = insertion.on_conflict_do_nothing(index_elements=list(table.columns.keys()))
            if on_conflict_columns:
                insertion = insertion.on_conflict_do_nothing(index_elements=on_conflict_columns)
            conn.execute(insertion)
            conn.commit()
            successful_inserts += 1
        except Exception as e:
            failed_inserts += 1
            log_error(
                error_type=type(e).__name__,
                error_message=str(e),
                table_name=table_name,
                row_data=row,
                sql_query=str(insertion)
            )
            conn.rollback()
            continue
    
    logging.info(f"Table: {table_name} - Operation completed. {successful_inserts} rows successful, {failed_inserts} rows failed.")
    return successful_inserts, failed_inserts

def does_exist(data, column_name, table_name, conn=conn):
    result = conn.execute(text(f"SELECT EXISTS (SELECT 1 FROM {table_name} WHERE {column_name} = {data})"))  # eğer :{data} olursa %(52)s gibi bi şey oluyor
    exist = result.scalar()
    return exist
    

def fetch_data(column_name, table_name, engine = engine, conn = conn) -> list:
    """
    Kolon ve tablo bilgisine göre veritabanından veriler çekilir. Liste döner.
    """
    metadata = MetaData()
    match_table = Table(table_name, metadata, autoload_with=engine)
    stmt = select(match_table.c[column_name])
    result = conn.execute(stmt).fetchall()
    data = [row[0] for row in result]

    return data
