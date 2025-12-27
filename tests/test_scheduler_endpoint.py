from fastapi.testclient import TestClient
from api.main import app
from datetime import date
import json

client = TestClient(app)

def test_generate_schedule():
    """
    Test the /schedule endpoint with valid data.
    """
    payload = {
        "latitude": 51.5074,
        "longitude": -0.1278,
        "date": date.today().isoformat(),
        "timezone": "Europe/London",
        "method": "MWL",
        "tasks": [
            {"name": "Complete Project Proposal", "duration_minutes": 120, "type": "deep"},
            {"name": "Email Client", "duration_minutes": 30, "type": "shallow"},
            {"name": "Code Review", "duration_minutes": 60, "type": "deep"}
        ]
    }
    
    response = client.post("/schedule", json=payload)
    assert response.status_code == 200, f"Failed: {response.text}"
    
    data = response.json()
    print("Response keys:", data.keys())
    assert "schedule" in data
    assert "prayer_times" in data
    
    schedule = data['schedule']
    assert len(schedule) > 0
    
    # Check if tasks were assigned (simple check based on logic)
    deep_work_block = next((b for b in schedule if b['type'] == 'work_deep'), None)
    assert deep_work_block is not None
    assert "tasks" in deep_work_block
    # Check if deep work tasks are present
    task_names = [t['name'] for t in deep_work_block['tasks']]
    assert "Complete Project Proposal" in task_names

    print("Test passed!")
    print(json.dumps(schedule, indent=2))

if __name__ == "__main__":
    test_generate_schedule()
