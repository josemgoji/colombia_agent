from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List

class TextChunker:
    """
    Clase que se encarga de dividir texto plano en fragmentos
    más pequeños para ser indexados eficientemente en la base vectorial.
    """

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " "]
        )

    def chunk_text(self, text: str) -> List[str]:
        return self.splitter.split_text(text)
