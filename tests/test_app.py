from app import app, tasks


def test_home_page():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert "ToDo Task Manager" in response.text


def test_add_task():
    client = app.test_client()
    tasks.clear()

    response = client.post("/", data={"task": "Test task"}, follow_redirects=True)

    assert response.status_code == 200
    assert "Test task" in response.text


def test_health_check():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}