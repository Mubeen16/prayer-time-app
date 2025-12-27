from fastapi.testclient import TestClient
from api.main import app
import os

client = TestClient(app)

def test_static_files():
    # 1. Test Root (index.html)
    response = client.get("/")
    assert response.status_code == 200
    assert "Rafeeq" in response.text
    assert "Faith & Flow State" in response.text
    print("Root (index.html) loaded successfully.")

    # 2. Test CSS
    response = client.get("/static/style.css")
    assert response.status_code == 200
    assert ":root" in response.text
    print("CSS loaded successfully.")

    # 3. Test JS
    response = client.get("/static/app.js")
    assert response.status_code == 200
    assert "generateSchedule" in response.text
    print("JS loaded successfully.")

if __name__ == "__main__":
    test_static_files()
