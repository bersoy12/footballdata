import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import create_engine, MetaData, Table, text, select
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('SOFA_URI'))
conn = engine.connect()

def truncate_table(table_name, conn=conn):
    conn.execute(text("TRUNCATE TABLE {} CASCADE;".format(table_name)))
    conn.commit()


def insert_table(df, table_name, engine = engine, conn = conn, on_conflict_columns: list = []):
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=engine)
    
    df = df.where(pd.notnull(df), None)
    df = df.replace({pd.NA: None, pd.NaT: None})
    
    rows = df.to_dict(orient='records')
    
    successful_inserts = 0
    failed_inserts = 0
    
    for row in rows:
        try:
            insertion = insert(table).values(row)
            if on_conflict_columns:
                insertion = insertion.on_conflict_do_nothing(index_elements=on_conflict_columns)
            conn.execute(insertion)
            conn.commit()
            successful_inserts += 1
        except Exception as e:
            print(f"Satır eklenirken hata oluştu: {str(e)}")
            print(f"Hatalı satır: {row}")
            failed_inserts += 1
            conn.rollback()
            continue
    
    print(f"Toplam {len(rows)} satırdan {successful_inserts} başarıyla eklendi, {failed_inserts} satır atlandı.")

def does_exist(data, column_name, table_name, conn=conn):
    result = conn.execute(text(f"SELECT EXISTS (SELECT 1 FROM {table_name} WHERE {column_name} = {data})"))  # eğer :{data} olursa %(52)s gibi bi şey oluyor
    exist = result.scalar()
    return exist
    

def fetch_data(column_name, table_name, engine = engine, conn = conn) -> list:
    metadata = MetaData()
    match_table = Table(table_name, metadata, autoload_with=engine)
    stmt = select(match_table.c[column_name])
    result = conn.execute(stmt).fetchall()
    data = [row[0] for row in result]

    return data
