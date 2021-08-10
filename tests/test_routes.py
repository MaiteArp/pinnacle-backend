from app.models.user import User


def test_create_user(client, one_user):
    #Act
    response = client.post("/app/users", json={
        "name": "Bob",
        "password": "Ross"
    })
    response_body = response.get_json()
    #Assert
    assert response.status_code == 201
    assert "user" in response_body
    


# def test_get_one_user(client, one_user):
#     #Act
#     response = client.get("/users")
#     response_body = response.get_json()
#     #Assert
#     assert response.status_code == 200
#     assert len(response_body) == 1
#     assert response_body == [
#         {
#             "user_id": 1,
#             "name": "Bob",
#             "password": "Ross",
#     }
# ]