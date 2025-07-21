import os
import logging

from langchain_community.vectorstores import Chroma
from langchain.schema.retriever import BaseRetriever

from src.rag.vector_store import VectorStoreManager
from src.rag.prepare_data import prepare_data
from src.config.env import settings

logger = logging.getLogger(__name__)

class RetrieverFactory:
    """
    Clase encargada de generar un retriever a partir de la base vectorial.
    """

    def __init__(self, persist_path: str = None):
        self.persist_path = persist_path or settings.CHROMA_DB_PATH
        self.vector_store = self._load_vector_store()

    def _load_vector_store(self) -> Chroma:
        """
        Carga la base vectorial desde disco.
        """
        if not os.path.exists(self.persist_path):
            logger.warning("Base vectorial no encontrada. Creando una nueva...")
            prepare_data(self.persist_path)
            
        else:
            logger.info("Base vectorial encontrada en disco.")
        
        manager = VectorStoreManager(persist_path=self.persist_path)
        return manager.load_vector_store()

    def get_retriever(self, k: int = 3) -> BaseRetriever:
        """
        Devuelve un retriever listo para usar.
        """
        return self.vector_store.as_retriever(search_kwargs={"k": k})