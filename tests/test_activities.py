"""Tests for the activities endpoint."""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 8
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert "Basketball Team" in data
    assert "Soccer Club" in data
    assert "Art Club" in data
    assert "Drama Club" in data
    assert "Debate Club" in data


def test_get_activities_returns_correct_structure(client):
    """Test that each activity has the required fields."""
    response = client.get("/activities")
    data = response.json()
    
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    for activity_name, activity_details in data.items():
        assert isinstance(activity_details, dict)
        assert required_fields.issubset(activity_details.keys())
        assert isinstance(activity_details["description"], str)
        assert isinstance(activity_details["schedule"], str)
        assert isinstance(activity_details["max_participants"], int)
        assert isinstance(activity_details["participants"], list)


def test_get_activities_chess_club_has_initial_participants(client):
    """Test that Chess Club has the expected initial participants."""
    response = client.get("/activities")
    data = response.json()
    
    chess_club = data["Chess Club"]
    assert chess_club["max_participants"] == 12
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]
    assert len(chess_club["participants"]) == 2


def test_get_activities_empty_activity_has_no_participants(client):
    """Test that newly created activities with no participants show empty list."""
    response = client.get("/activities")
    data = response.json()
    
    basketball_team = data["Basketball Team"]
    assert basketball_team["participants"] == []
    assert basketball_team["max_participants"] == 15
