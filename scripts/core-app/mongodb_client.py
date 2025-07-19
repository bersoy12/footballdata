from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import os
from dotenv import load_dotenv
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

load_dotenv()

# Logging setup
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)

class MongoDBClient:
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Cloud MongoDB bağlantısını kurar"""
        try:
            # Cloud MongoDB connection string (MongoDB Atlas veya diğer cloud provider)
            mongo_connection_string = os.getenv('MONGO_CONNECTION_STRING')
            
            if not mongo_connection_string:
                logger.error("MONGO_CONNECTION_STRING environment variable bulunamadı!")
                return
                # raise ValueError("MONGO_CONNECTION_STRING gerekli")
            
            # MongoDB client oluştur
            self.client = MongoClient(mongo_connection_string, serverSelectionTimeoutMS=10000)
            
            # Bağlantıyı test et
            try:
                self.client.admin.command('ping')
                logger.info("Cloud MongoDB bağlantısı başarılı")
                mongo_database = os.getenv('MONGO_DATABASE', 'football_raw')
                self.db = self.client[mongo_database]
            except Exception as ping_err:
                logger.error(f"MongoDB ping başarısız: {ping_err}")
                self.client = None
                self.db = None
            
        except Exception as e:
            self.client = None
            self.db = None
        
    def serialize_mongo_document(self, doc):
        doc = dict(doc)
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc
    
    def insert_raw_data(self, collection_name: str, data: Dict[str, Any]) -> bool:
        """
        Ham JSON verisini MongoDB'ye ekler
        
        Args:
            collection_name: Koleksiyon adı
            data: Eklenecek veri (dict)
        
        Returns:
            bool: İşlem başarılı mı
        """
        try:
            if not self.db:
                self.connect()
            
            # Timestamp ekle
            data['inserted_at'] = datetime.now()
            
            collection = self.db[collection_name]
            result = collection.insert_one(data)
            
            logger.info(f"Raw data inserted to {collection_name}: {result.inserted_id}")
            return True
            
        except Exception as e:
            logger.error(f"Raw data insertion error in {collection_name}: {e}")
            return False
    
    def insert_bulk_raw_data(self, collection_name: str, data_list: List[Dict[str, Any]], conflict_column: str = "") -> Dict[str, int]:
        """
        Birden fazla ham JSON verisini MongoDB'ye toplu olarak ekler
        
        Args:
            collection_name: Koleksiyon adı
            data_list: Eklenecek veri listesi
        
        Returns:
            Dict: Başarılı ve başarısız işlem sayıları
        """
        try:
            if self.db is None:
                self.connect()
            
            if collection_name not in self.db.list_collection_names():
                self.db.create_collection(collection_name)
                logger.info(f"Collection '{collection_name}' created manually.")

            for data in data_list:
                data['inserted_at'] = datetime.now()
            
            collection = self.db[collection_name]
            result = collection.insert_many(data_list, ordered=False)
            
            logger.info(f"Bulk raw data inserted to {collection_name}: {len(result.inserted_ids)} documents")
            return {"successful": len(result.inserted_ids), "failed": 0}
            
        except Exception as e:
            logger.error(f"Bulk raw data insertion error in {collection_name}: {e}")
            return {"successful": 0, "failed": len(data_list)}
    
    def get_raw_data(self, collection_name: str
                     , query: Dict[str, Any] = None
                     , projection: Dict[str, Any] = None
                     , limit: int = 100) -> List[Dict[str, Any]]:
        """
        MongoDB'den ham veri çeker
        
        Args:
            collection_name: Koleksiyon adı
            query: Sorgu filtresi
            limit: Maksimum dönecek döküman sayısı
        
        Returns:
            List: Veri listesi
        """
        try:
            if self.db is None:
                self.connect()
            
            collection = self.db[collection_name]
            
            if query is None:
                query = {}
            
            cursor = (
                collection.find(query, projection).limit(limit)
                if projection 
                else collection.find(query).limit(limit)
            )

            data = [self.serialize_mongo_document(doc) for doc in cursor]
            
            logger.info(f"Raw data retrieved from {collection_name}: {len(data)} documents")
            return data
            
        except Exception as e:
            logger.error(f"Raw data retrieval error from {collection_name}: {e}")
            return []
    
    def update_raw_data(self, collection_name: str, filter_query: Dict[str, Any], update_data: Dict[str, Any]) -> bool:
        """
        MongoDB'deki ham veriyi günceller
        
        Args:
            collection_name: Koleksiyon adı
            filter_query: Güncellenecek dökümanı bulmak için filtre
            update_data: Güncellenecek veri
        
        Returns:
            bool: İşlem başarılı mı
        """
        try:
            if not self.db:
                self.connect()
            
            collection = self.db[collection_name]
            
            # Timestamp ekle
            update_data['updated_at'] = datetime.now()
            
            result = collection.update_one(filter_query, {'$set': update_data})
            
            logger.info(f"Raw data updated in {collection_name}: {result.modified_count} documents")
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Raw data update error in {collection_name}: {e}")
            return False
    
    def delete_raw_data(self, collection_name: str, filter_query: Dict[str, Any]) -> bool:
        """
        MongoDB'den ham veri siler
        
        Args:
            collection_name: Koleksiyon adı
            filter_query: Silinecek dökümanı bulmak için filtre
        
        Returns:
            bool: İşlem başarılı mı
        """
        try:
            if not self.db:
                self.connect()
            
            collection = self.db[collection_name]
            result = collection.delete_one(filter_query)
            
            logger.info(f"Raw data deleted from {collection_name}: {result.deleted_count} documents")
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Raw data deletion error in {collection_name}: {e}")
            return False
    
    def get_collections(self) -> List[str]:
        """
        Veritabanındaki tüm koleksiyonları listeler
        
        Returns:
            List: Koleksiyon adları listesi
        """
        try:
            if not self.db:
                self.connect()
            
            collections = self.db.list_collection_names()
            logger.info(f"Collections retrieved: {collections}")
            return collections
            
        except Exception as e:
            logger.error(f"Collections retrieval error: {e}")
            return []
    
    def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """
        Koleksiyon istatistiklerini getirir
        
        Args:
            collection_name: Koleksiyon adı
        
        Returns:
            Dict: Koleksiyon istatistikleri
        """
        try:
            if not self.db:
                self.connect()
            
            collection = self.db[collection_name]
            stats = self.db.command("collstats", collection_name)
            
            return {
                "collection_name": collection_name,
                "document_count": stats.get("count", 0),
                "size_bytes": stats.get("size", 0),
                "avg_document_size": stats.get("avgObjSize", 0)
            }
            
        except Exception as e:
            logger.error(f"Collection stats error for {collection_name}: {e}")
            return {}
    
    def close(self):
        """MongoDB bağlantısını kapatır"""
        if self.client:
            self.client.close()
            logger.info("MongoDB bağlantısı kapatıldı")



mongodb_client = MongoDBClient()