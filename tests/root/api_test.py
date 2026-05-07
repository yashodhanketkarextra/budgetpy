class TestPublicRoot:
    def test_read_root(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}

    def test_add_root(self, client):
        response = client.post("/add", json={"first": 1, "second": 2})
        assert response.status_code == 200
        assert response.json() == {"result": 3}

    def test_add_root_invalid(self, client):
        response = client.post("/add", json={"first": 1, "second": "a"})
        assert response.status_code == 422
