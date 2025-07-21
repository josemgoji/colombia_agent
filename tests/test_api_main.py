from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api.main import app, agent

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_ask_empty_question():
    payload = {"question": "   "}
    response = client.post("/ask", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "La pregunta no puede estar vacia."

def test_ask_valid_question():
    with patch.object(agent, "ask", return_value="Respuesta de prueba"):
        payload = {"question": "¿Cuál es la capital de Colombia?"}
        response = client.post("/ask", json=payload)
        assert response.status_code == 200
        assert response.json()["answer"] == "Respuesta de prueba"

