def get_mock_user():
    return {
        "email": "user1@gmail.com",
        "firstName": "FirstName-User1",
        "lastName": "LastName-User1",
        "password": "mypass",
    }


def get_mock_user2():
    return {
        "email": "user2@gmail.com",
        "firstName": "FirstName-User2",
        "lastName": "LastName-User2",
        "password": "secret-password",
    }


def get_user_creds2():
    return {
        "email": "user2@gmail.com",
        "password": "secret-password",
    }


def get_user_creds():
    return {
        "email": "user1@gmail.com",
        "password": "mypass",
    }


def get_admin_creds():
    return {
        "email": "admin@myapp.com",
        "password": "admin",
    }


def get_admin_user():
    return {
        "email": "admin@myapp.com",
        "firstName": "admin",
        "lastName": "admin",
        "password": "admin",
        "role": "admin"
    }


def get_mock_users():
    return [
        {
            "email": "user1@gmail.com",
            "firstName": "FirstName-User1",
            "lastName": "LastName-User1",
            "password": "mypass",
        },
        {
            "email": "user2@gmail.com",
            "firstName": "FirstName-User2",
            "lastName": "LastName-User2",
            "password": "secret-password",
        }
    ]
