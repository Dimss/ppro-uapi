def get_mock_user():
    return {
        "email": "user1@gmail.com",
        "firstName": "FirstName-User1",
        "lastName": "LastName-User1",
        "password": "secret-password"
    }


def get_mock_users():
    return [
        {
            "email": "user1@gmail.com",
            "firstName": "FirstName-User1",
            "lastName": "LastName-User1",
            "password": "secret-password"
        },
        {
            "email": "user2@gmail.com",
            "firstName": "FirstName-User2",
            "lastName": "LastName-User2",
            "password": "secret-password"
        }
    ]
