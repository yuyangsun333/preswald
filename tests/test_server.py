from fastapi.testclient import TestClient
from preswald.server import app

client = TestClient(app)


def test_render_app(monkeypatch):
    # Mock the user script render function
    def mock_render():
        return "<h1>Mocked App</h1>"

    monkeypatch.setattr("user_script.render", mock_render)
    response = client.get("/")
    assert response.status_code == 200
    assert "<h1>Mocked App</h1>" in response.text


def test_handle_interaction():
    payload = {"type": "button_click", "data": "Submit"}
    response = client.post("/interact", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Button 'Submit' clicked!"
