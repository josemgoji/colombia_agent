import logging
from src.rag.loader import WikipediaScraper
from src.rag.vector_store import VectorStoreManager
from src.rag.text_splitter import TextChunker
from src.config.constants import WIKIPEDIA_URL
from src.config.env import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPreparator:
    def __init__(self, url: str = WIKIPEDIA_URL, chunk_size: int = 500, chunk_overlap: int = 100):
        self.url = url
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.scraper = WikipediaScraper(self.url)
        self.chunker = TextChunker(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        self.vector_store_manager = VectorStoreManager(persist_path=settings.CHROMA_DB_PATH)

    def prepare(self):
        logger.info("Scrapeando contenido desde Wikipedia...")
        self.scraper.fetch()
        text = self.scraper.extract_clean_text()
        logger.info("Scraping completado.")

        logger.info("Dividiendo texto en fragmentos (chunks)...")
        text_chunks = self.chunker.chunk_text(text)
        logger.info(f"{len(text_chunks)} fragmentos generados.")

        logger.info("Generando base vectorial...")
        self.vector_store_manager.create_vector_store(text_chunks)
        logger.info(f"✅ Base vectorial creada y guardada en: {settings.CHROMA_DB_PATH}")


def prepare_data():
    preparator = DataPreparator()
    preparator.prepare()


