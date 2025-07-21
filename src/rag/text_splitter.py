from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from src.config.constants import CHUNK_SIZE, CHUNK_OVERLAP

class TextChunker:
    """
    Clase que se encarga de dividir texto plano en fragmentos
    más pequeños para ser indexados eficientemente en la base vectorial.
    """

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", " "]
        )

    def chunk_text(self, text: str) -> List[str]:
        return self.splitter.split_text(text)
