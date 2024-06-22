import unittest
import datetime
from http import HTTPStatus
from flask import jsonify
from conftest import TestApp
from src.utils.jwt_manager import JWTManager  # Assuming your TestApp class is in test_app.py

class TestJWTManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_app = TestApp.get_instance()
        cls.app = cls.test_app.app
        cls.client = cls.test_app.client
        cls.jwt_manager:JWTManager = cls.app.jwt_manager

        # Define routes for testing
        @cls.app.route('/protected')
        @cls.jwt_manager.jwt_required
        def protected_route(identity):
            return jsonify(identity), HTTPStatus.OK
    
    @classmethod
    def tearDownClass(cls):
        TestApp.destruct_instance()

    def test_create_access_token(self):
        identity = {"username": "admin"}
        token = self.jwt_manager.create_access_token(identity)
        self.assertIsNotNone(token)

    def test_create_refresh_token(self):
        identity = {"username": "admin"}
        token = self.jwt_manager.create_refresh_token(identity)
        self.assertIsNotNone(token)

    def test_verify_access_jwt_in_request_valid(self):
        identity = {"username": "admin"}
        token = self.jwt_manager.create_access_token(identity)
        
        with self.app.test_request_context(headers={"Cookie": f"access_token={token}"}):
            verified_identity = self.jwt_manager.verify_access_jwt_in_request()
            self.assertEqual(verified_identity, identity)

    def test_verify_access_jwt_in_request_invalid(self):
        with self.app.test_request_context(headers={"Cookie": "access_token=invalid_token"}):
            verified_identity = self.jwt_manager.verify_access_jwt_in_request()
            self.assertFalse(verified_identity)

    def test_verify_refresh_jwt_in_request_valid(self):
        identity = {"username": "admin"}
        token = self.jwt_manager.create_refresh_token(identity)
        
        verified_token = self.jwt_manager.verify_refresh_jwt_in_request(token)
        self.assertIsNotNone(verified_token)
        self.assertEqual(verified_token['identity'], identity)

    def test_verify_refresh_jwt_in_request_invalid(self):
        verified_token = self.jwt_manager.verify_refresh_jwt_in_request("invalid_token")
        self.assertFalse(verified_token)

    def test_jwt_required_decorator_valid(self):
        identity = {"username": "admin"}
        token = self.jwt_manager.create_access_token(identity)
        self.client.set_cookie('access_token',token)
        response = self.client.get('/protected')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.get_json(), identity)

    def test_jwt_required_decorator_invalid(self):
        response = self.client.get('/protected', headers={"Cookie": "access_token=invalid_token"})
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_refresh_token_about_to_expire_true(self):
        curr_refresh_token = {
            "exp": datetime.datetime.now(datetime.timezone.utc).timestamp() + 30  # 30 seconds from now
        }
        self.assertTrue(self.jwt_manager.refresh_token_about_to_expire(curr_refresh_token))

    def test_refresh_token_about_to_expire_false(self):
        curr_refresh_token = {
            "exp": (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=2)).timestamp()
        }
        self.assertFalse(self.jwt_manager.refresh_token_about_to_expire(curr_refresh_token))

if __name__ == '__main__':
    unittest.main(verbosity=2)
