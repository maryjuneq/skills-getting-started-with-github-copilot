"""Tests for the signup endpoint."""

import pytest


def test_successful_signup(client):
    """Test that a student can successfully sign up for an activity."""
    response = client.post(
        "/activities/Basketball Team/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Basketball Team" in data["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds the email to the activity participants list."""
    email = "newstudent@mergington.edu"
    activity_name = "Basketball Team"
    
    # Signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data[activity_name]["participants"]


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signing up for a non-existent activity returns 404."""
    response = client.post(
        "/activities/Nonexistent Club/signup?email=student@mergington.edu"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_duplicate_signup_prevention(client):
    """Test that a student cannot sign up twice for the same activity.
    
    This test demonstrates the current bug where duplicate signups are allowed.
    """
    email = "duplicate@mergington.edu"
    activity_name = "Chess Club"
    
    # First signup
    response1 = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert response1.status_code == 200
    
    # Second signup (should fail, but currently succeeds - this is the bug)
    response2 = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    # This should return 400 after the fix, but currently returns 200
    assert response2.status_code == 400, "Duplicate signup should not be allowed"


def test_different_students_can_signup_for_same_activity(client):
    """Test that different students can sign up for the same activity."""
    activity_name = "Soccer Club"
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    # First student signs up
    response1 = client.post(
        f"/activities/{activity_name}/signup?email={email1}"
    )
    assert response1.status_code == 200
    
    # Second student signs up
    response2 = client.post(
        f"/activities/{activity_name}/signup?email={email2}"
    )
    assert response2.status_code == 200
    
    # Verify both are in participants
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email1 in participants
    assert email2 in participants
    assert len(participants) == 2


def test_student_can_signup_for_different_activities(client):
    """Test that a student can sign up for multiple different activities."""
    email = "multisigner@mergington.edu"
    
    response1 = client.post(
        f"/activities/Chess Club/signup?email={email}"
    )
    assert response1.status_code == 200
    
    response2 = client.post(
        f"/activities/Drama Club/signup?email={email}"
    )
    assert response2.status_code == 200
    
    # Verify student is in both activities
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data["Chess Club"]["participants"]
    assert email in activities_data["Drama Club"]["participants"]


def test_signup_response_message_format(client):
    """Test that the response message has the correct format."""
    email = "responsetest@mergington.edu"
    activity = "Gym Class"
    
    response = client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    # Message should mention both email and activity name
    message = data["message"].lower()
    assert email.lower() in message
    assert activity.lower() in message
