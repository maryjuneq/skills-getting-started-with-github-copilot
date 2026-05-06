"""Pytest configuration and fixtures for FastAPI tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def test_activities():
    """Provide a fresh set of test activities data."""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Practice and compete in basketball games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": []
        },
        "Soccer Club": {
            "description": "Train and play soccer matches",
            "schedule": "Wednesdays and Saturdays, 3:00 PM - 5:00 PM",
            "max_participants": 22,
            "participants": []
        },
        "Art Club": {
            "description": "Explore painting, drawing, and other visual arts",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": []
        },
        "Drama Club": {
            "description": "Act in plays and learn theater skills",
            "schedule": "Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 20,
            "participants": []
        },
        "Debate Club": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": []
        }
    }


@pytest.fixture
def client(test_activities):
    """Reset activities and provide TestClient for each test."""
    # Reset the global activities dict with fresh test data
    activities.clear()
    activities.update(test_activities)
    
    return TestClient(app)
