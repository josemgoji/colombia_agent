import pytest
from src.agent.wiki_agent import WikiAgent


@pytest.fixture(scope="module")
def agent():
    return WikiAgent()


def test_agent_instance_is_correct(agent):
    assert isinstance(agent, WikiAgent)


def test_answer_is_valid_for_colombia(agent):
    question = "¿Cuál es la capital de Colombia?"
    answer = agent.ask(question)

    assert isinstance(answer, str)
    assert len(answer.strip()) > 0
    assert "no tengo información suficiente" not in answer.lower()

