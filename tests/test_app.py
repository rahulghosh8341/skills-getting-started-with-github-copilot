from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # Some known activity from the in-memory DB
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "test.user+pytest@example.com"

    # Ensure clean starting state for this email
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    res = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 200
    assert email in activities[activity]["participants"]

    # Signing up again should fail (already signed up)
    res_dup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res_dup.status_code == 400

    # Unregister
    res_unreg = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert res_unreg.status_code == 200
    assert email not in activities[activity]["participants"]

    # Unregistering again should return 404
    res_unreg2 = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert res_unreg2.status_code == 404
