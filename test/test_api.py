import unittest
from uapi.app.users import DB
from uapi.conf import conf
from uapi.app.bootstrap import populate_system_data
from .datamock import *
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
        populate_system_data()

    def setUp(self):
        # Setup the WebTest
        self.app = TestApp(run.api)

    def tearDown(self):
        # Cleanup configs collection before each test
        conn = DB.get_db_conn()[conf.DB_NAME]
        conn.users.drop()
        populate_system_data()

    def test_create_new_user(self):
        user = get_mock_user()
        res = self.app.post_json("/user", user)
        new_user = json.loads(res.body)
        user['role'] = 'user'
        del (user['password'])
        self.assertEqual(new_user['data'], user)

    def test_create_bad_schema_twice(self):
        user = get_mock_user()
        del (user['password'])
        self.app.post_json("/user", user, status=falcon.HTTP_406)

    def test_create_same_user_twice(self):
        self.app.post_json("/user", get_mock_user())
        self.app.post_json("/user", get_mock_user(), status=falcon.HTTP_409)

    def test_list_users_as_admin(self):
        token = json.loads(self.app.post_json("/jwt", get_admin_creds()).body)
        user_list = get_mock_users()
        for user in user_list:
            self.app.post_json("/user", user)
            del (user['password'])
            user['role'] = 'user'
        res = json.loads(self.app.get("/user", headers={'X-UAPI-AUTH': token['data']['token']}).body)
        i = 0
        # Remove admin user from the users list before compare the results
        for user in res['data']:
            if user['role'] == 'admin':
                del res['data'][i]
            i += 1
        self.assertEqual(res['data'], user_list)

    def test_list_users_as_user(self):
        user_list = get_mock_users()
        for user in user_list:
            self.app.post_json("/user", user)
            del (user['password'])
            user['role'] = 'user'
        token = json.loads(self.app.post_json("/jwt", get_user_creds()).body)
        res = json.loads(self.app.get("/user", headers={'X-UAPI-AUTH': token['data']['token']}).body)
        user = get_mock_user()
        del user['password']
        user['role'] = 'user'
        self.assertEqual(res['data'], user)

    def test_get_user(self):
        user = get_mock_user()
        self.app.post_json("/user", user)
        del (user['password'])
        token = json.loads(self.app.post_json("/jwt", get_user_creds()).body)
        res = json.loads(self.app.get(f"/user/{user['email']}", headers={'X-UAPI-AUTH': token['data']['token']}).body)
        user['role'] = 'user'
        self.assertEqual(res['data'], user)

    def test_update_user_as_user(self):
        user = get_mock_user()
        email = user['email']
        self.app.post_json("/user", user)
        token = json.loads(self.app.post_json("/jwt", get_user_creds()).body)
        del (user['password'])
        del (user['email'])
        user['firstName'] = "newFirstName"
        user['lastName'] = "newLastName"
        self.app.put_json(f"/user/{email}", user, headers={'X-UAPI-AUTH': token['data']['token']})
        res = json.loads(self.app.get(f"/user/{email}", headers={'X-UAPI-AUTH': token['data']['token']}).body)
        user['email'] = email
        user['role'] = 'user'
        self.assertEqual(res['data'], user)

    def test_update_user_as_other_user(self):
        user = get_mock_user()
        email = user['email']
        self.app.post_json("/user", user)
        self.app.post_json("/user", get_mock_user2())
        token = json.loads(self.app.post_json("/jwt", get_user_creds2()).body)
        del (user['password'])
        del (user['email'])
        user['firstName'] = "newFirstName"
        user['lastName'] = "newLastName"
        self.app.put_json(f"/user/{email}", user, headers={'X-UAPI-AUTH': token['data']['token']},
                          status=falcon.HTTP_403)

    def test_delete_user_as_user(self):
        user = get_mock_user()
        self.app.post_json("/user", user)
        res = json.loads(self.app.post_json("/jwt", get_user_creds()).body)
        self.app.delete(f"/user/{user['email']}", headers={'X-UAPI-AUTH': res['data']['token']}, status=falcon.HTTP_403)

    def test_delete_user_as_admin(self):
        user = get_mock_user()
        self.app.post_json("/user", user)
        res = json.loads(self.app.post_json("/jwt", get_admin_creds()).body)
        self.app.delete(f"/user/{user['email']}", headers={'X-UAPI-AUTH': res['data']['token']})
        self.app.get(f"/user/{user['email']}", headers={'X-UAPI-AUTH': res['data']['token']}, status=falcon.HTTP_404)

    def test_create_jwt_token(self):
        user = get_mock_user()
        self.app.post_json("/user", user)
        json.loads(self.app.post_json("/jwt", get_user_creds()).body)

    def test_access_to_private_resource(self):
        self.app.get("/user/bla", status=falcon.HTTP_401)


if __name__ == '__main__':
    unittest.main()
