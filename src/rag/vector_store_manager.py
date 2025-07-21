from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema.document import Document
from typing import List
import os

from src.config.settings import settings


class VectorStoreManager:
    """
    Clase encargada de construir o cargar una base vectorial usando ChromaDB.
    Usa modelos open source de HuggingFace para generar embeddings.
    """

    def __init__(self, persist_path: str = None):
        self.persist_path = persist_path or settings.CHROMA_DB_PATH
        self.embedding_model_name = settings.EMBEDDING_MODEL
        self.embedding = HuggingFaceEmbeddings(model_name=self.embedding_model_name)

    def create_vector_store(self, texts: List[str]) -> Chroma:
        """
        Crea y guarda una base vectorial con los textos dados.
        
        Args:
            texts (List[str]): Lista de textos a indexar.
            
        Returns:
            Chroma: Instancia de la base vectorial creada.
        """
        documents = [Document(page_content=txt) for txt in texts]

        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embedding,
            persist_directory=self.persist_path
        )

        return vector_store

    def load_vector_store(self) -> Chroma:
        """
        Carga una base vectorial persistente desde disco.
        """
        if not os.path.exists(self.persist_path):
            raise FileNotFoundError(f"No se encontró la base vectorial en: {self.persist_path}")

        return Chroma(
            embedding_function=self.embedding,
            persist_directory=self.persist_path
        )
