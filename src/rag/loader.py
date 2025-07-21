import requests
from bs4 import BeautifulSoup
from typing import Optional


class WikipediaScraper:
    """
    Clase para hacer scraping a una página de Wikipedia
    Extrae y limpia contenido textual.
    """

    def __init__(self, url: str):
        self.url = url
        self.soup: Optional[BeautifulSoup] = None

    def fetch(self) -> None:
        """
        Descarga el contenido HTML de la página.
        """
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            raise RuntimeError(f"Error al hacer scraping: {e}")

    def extract_clean_text(self) -> str:
        """
        Extrae y limpia el texto del artículo principal de Wikipedia.
        Retorna el texto plano.
        """
        if not self.soup:
            raise ValueError("Debes ejecutar 'fetch()' primero.")

        # Encuentra el contenido principal
        content_div = self.soup.find("div", {"id": "mw-content-text"})
        if not content_div:
            raise ValueError("No se pudo encontrar el contenido principal.")

        # Extrae los párrafos relevantes
        paragraphs = content_div.find_all("p")
        cleaned_paragraphs = []

        for p in paragraphs:
            text = p.get_text(separator=" ", strip=True)
            if text:
                cleaned_paragraphs.append(text)

        full_text = "\n".join(cleaned_paragraphs)
        return self._clean_text(full_text)

    def _clean_text(self, text: str) -> str:
        """
        Limpia referencias tipo [1], [2], espacios dobles, etc.
        """
        import re

        # Elimina referencias entre corchetes tipo [1]
        text = re.sub(r"\[\d+\]", "", text)

        # Reemplaza múltiples espacios por uno
        text = re.sub(r"\s+", " ", text)

        return text.strip()