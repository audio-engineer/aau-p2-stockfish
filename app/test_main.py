"""Test suite for the main application"""

from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_evaluate_position():
    """Test whether normal input yields normal output"""

    response = client.post(
        "/evaluate-position",
        json={"fen": "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"},
    )

    assert response.status_code == 200


def test_evaluate_position_with_time_to_analyze():
    """Test whether normal input with a non-default timeToAnalyze value yields
    normal output"""

    response = client.post(
        "/evaluate-position",
        json={
            "fen": "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2",
            "timeToAnalyze": 3000,
        },
    )

    assert response.status_code == 200


def test_analyze_move_invalid_fen():
    """Test whether an invalid FEN raises an error and returns status 400"""

    response = client.post(
        "/analyze-move",
        json={
            "fen": "3q4/8/1PpPp3/2BP4/p1Pp4/1b2kP1r/1N6/K8 w - - 0 1",
            "move": "f3f4",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid FEN"}


def test_analyze_move_invalid_move():
    """Test whether an invalid move raises an error and returns status 400"""

    response = client.post(
        "/analyze-move",
        json={
            "fen": "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2",
            "move": "a2a1",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid move"}
