from test.ustils.task import create_random_task


def test_should_fetch_task_create(client, db_session):
    task = create_random_task(db=db_session)
    response = client.get(f"/task/{task.id}")
    assert response.status_code == 200
    assert response.json()["title"] == task.title
