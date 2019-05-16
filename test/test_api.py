import unittest
from uapi.app.users import DB
from uapi.conf import conf
from .datamock import get_mock_user, get_mock_users
from webtest import TestApp
from uapi import run
import falcon
import json


class TestAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Make sure the collection is empty before starting the tests
        conn = DB.get_db_conn()[conf.DB_NAME]
        conn.users.drop()

    def setUp(self):
        # Setup the WebTest
        self.app = TestApp(run.api)

    def tearDown(self):
        # Cleanup configs collection before each test
        conn = DB.get_db_conn()[conf.DB_NAME]
        conn.users.drop()

    def test_create_new_user(self):
        user = get_mock_user()
        res = self.app.post_json("/user", user)
        new_user = json.loads(res.body)
        del (user['password'])
        self.assertEqual(new_user['data'], user)

    def test_create_bad_schema_twice(self):
        user = get_mock_user()
        del (user['password'])
        self.app.post_json("/user", user, status=falcon.HTTP_406)

    def test_create_same_user_twice(self):
        self.app.post_json("/user", get_mock_user())
        self.app.post_json("/user", get_mock_user(), status=falcon.HTTP_409)

    def test_list_users(self):
        user_list = get_mock_users()
        for user in user_list:
            self.app.post_json("/user", user)
            del (user['password'])
        res = json.loads(self.app.get("/user").body)
        self.assertEqual(res['data'], user_list)

    def test_get_user(self):
        user = get_mock_user()
        self.app.post_json("/user", user)
        del (user['password'])
        res = json.loads(self.app.get(f"/user/{user['email']}").body)
        self.assertEqual(res['data'], user)

    def test_update_user(self):
        user = get_mock_user()
        email = user['email']
        self.app.post_json("/user", user)
        del (user['password'])
        del (user['email'])
        user['firstName'] = "newFirstName"
        user['lastName'] = "newLastName"
        self.app.put_json(f"/user/{email}", user)
        res = json.loads(self.app.get(f"/user/{email}").body)
        user['email'] = email
        self.assertEqual(res['data'], user)

    def test_delete_user(self):
        user = get_mock_user()
        self.app.post_json("/user", user)
        self.app.delete(f"/user/{user['email']}")
        self.app.get(f"/user/{user['email']}", status=falcon.HTTP_404)


if __name__ == '__main__':
    unittest.main()
