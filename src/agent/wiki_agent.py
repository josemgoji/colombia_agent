from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint

from src.rag.retriever_factory import RetrieverFactory
from src.config.settings import settings
from src.config.constants import PROMPT_TEMPLATE_PATH
from pathlib import Path


class WikiAgent:
    """
    Clase principal del agente que usa RAG para responder preguntas
    sobre el contenido de Wikipedia de Colombia.
    """

    def __init__(self):
        self.retriever = RetrieverFactory().get_retriever()
        self.llm = self._load_llm()
        self.prompt = self._load_prompt_template()
        self.chain = self._build_chain()
        
        
    def _load_llm(self):
        return HuggingFaceEndpoint(
            repo_id=settings.HF_REPO_ID, 
            temperature=settings.HF_TEMPERATURE,
            max_new_tokens=settings.HF_MAX_TOKENS,
            huggingfacehub_api_token=settings.HF_TOKEN,
            provider=settings.HF_PROVIDER
        )


    def _load_prompt_template(self) -> PromptTemplate:
        """
        Carga el prompt desde un archivo de texto.
        """
        prompt_path = Path(PROMPT_TEMPLATE_PATH)
        prompt_str = prompt_path.read_text(encoding="utf-8")

        return PromptTemplate(
            input_variables=["context", "question"],
            template=prompt_str
        )

    def _build_chain(self):
        """
        Construye la cadena RAG completa con retriever + LLM + prompt.
        """
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": self.prompt},
            return_source_documents=False
        )

    def ask(self, question: str) -> str:
        """
        Ejecuta la consulta contra la cadena RAG.
        """
        result = self.chain.invoke({"query": question})
        return result.get("result", "No se encontró una respuesta.")
