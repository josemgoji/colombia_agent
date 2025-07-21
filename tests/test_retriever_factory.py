import pytest
from langchain.schema.retriever import BaseRetriever
from src.rag.retriever_factory import RetrieverFactory


@pytest.fixture(scope="module")
def retriever():
    factory = RetrieverFactory()
    return factory.get_retriever(k=3)


def test_retriever_instance(retriever):
    """
    Verifica que el objeto retornado sea un retriever válido.
    """
    assert isinstance(retriever, BaseRetriever)


def test_retriever_returns_documents(retriever):
    """
    Verifica que el retriever pueda encontrar documentos relevantes.
    """
    query = "¿Cuál es la capital de Colombia?"
    docs = retriever.invoke(query)
    
    assert isinstance(docs, list)
    assert len(docs) > 0
    assert any("colombia" in doc.page_content.lower() for doc in docs)
