"""Integration tests for multi-step workflows."""

import pytest


def test_signup_workflow_fetch_then_signup(client):
    """Test the complete workflow: fetch activities, then signup."""
    # Step 1: Fetch activities
    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    activities_data = activities_response.json()
    assert "Chess Club" in activities_data
    
    initial_participants = activities_data["Chess Club"]["participants"].copy()
    
    # Step 2: Signup for an activity
    email = "workflow@mergington.edu"
    signup_response = client.post(
        f"/activities/Chess Club/signup?email={email}"
    )
    assert signup_response.status_code == 200
    
    # Step 3: Verify the participant was added
    verify_response = client.get("/activities")
    verify_data = verify_response.json()
    
    assert email in verify_data["Chess Club"]["participants"]
    assert len(verify_data["Chess Club"]["participants"]) == len(initial_participants) + 1


def test_multiple_signups_update_participant_count(client):
    """Test that multiple signups correctly update activity participant count."""
    activity = "Drama Club"
    
    # Get initial count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity]["participants"])
    
    # Signup 3 students
    emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
    
    for email in emails:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
    
    # Verify final count
    final_response = client.get("/activities")
    final_count = len(final_response.json()[activity]["participants"])
    
    assert final_count == initial_count + 3
    
    # Verify all emails are present
    final_participants = final_response.json()[activity]["participants"]
    for email in emails:
        assert email in final_participants


def test_signup_multiple_activities_creates_correct_list(client):
    """Test that a student signing up for multiple activities appears in all of them."""
    email = "multiactivity@mergington.edu"
    activities = ["Chess Club", "Drama Club", "Soccer Club"]
    
    # Signup for all activities
    for activity in activities:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
    
    # Verify student appears in all activities
    final_response = client.get("/activities")
    final_data = final_response.json()
    
    for activity in activities:
        assert email in final_data[activity]["participants"]


def test_signup_preserves_existing_participants(client):
    """Test that signup doesn't lose existing participants."""
    activity = "Programming Class"
    
    # Get existing participants
    initial_response = client.get("/activities")
    existing_participants = initial_response.json()[activity]["participants"].copy()
    
    # Add new participant
    new_email = "newprogrammer@mergington.edu"
    signup_response = client.post(
        f"/activities/{activity}/signup?email={new_email}"
    )
    assert signup_response.status_code == 200
    
    # Verify all participants (old + new) are present
    final_response = client.get("/activities")
    final_participants = final_response.json()[activity]["participants"]
    
    for existing_email in existing_participants:
        assert existing_email in final_participants
    assert new_email in final_participants
    assert len(final_participants) == len(existing_participants) + 1


def test_invalid_activity_doesnt_affect_participant_lists(client):
    """Test that a failed signup for invalid activity doesn't corrupt data."""
    activity = "Chess Club"
    
    # Get initial state
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()[activity]["participants"].copy()
    
    # Try to signup for non-existent activity
    response = client.post(
        "/activities/Nonexistent Activity/signup?email=test@mergington.edu"
    )
    assert response.status_code == 404
    
    # Verify Chess Club participants unchanged
    verify_response = client.get("/activities")
    verify_participants = verify_response.json()[activity]["participants"]
    
    assert verify_participants == initial_participants
