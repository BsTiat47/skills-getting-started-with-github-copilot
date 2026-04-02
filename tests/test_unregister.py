def test_unregister_success_removes_student(client):
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        f"Unregistered {existing_email} from {activity_name}"
    )

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert existing_email not in participants


def test_unregister_fails_for_missing_activity(client):
    response = client.delete(
        "/activities/Unknown Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_fails_for_student_not_signed_up(client):
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "not.signed.up@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up"
