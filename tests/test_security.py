
def test_login(client):
    data = {"username":"User","password":"123"}
    response = client.post("/login", data=data)
    assert response.status == '302 FOUND'