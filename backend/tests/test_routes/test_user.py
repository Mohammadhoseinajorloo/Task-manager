def test_create_user(client):
    data = {"email": "mohammadhoseinajorloo76@gmail.com", "username": "mohammad", "password": "12345678"}
    response = client.post("/users", json=data)
    assert response.status_code == 201
    assert response.json()["email"] == "mohammadhoseinajorloo76@gmail.com"
    assert response.json()["username"] == "mohammad"
    assert response.json()["password"] == "12345678"
