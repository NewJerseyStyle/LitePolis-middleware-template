import unittest
import base64
from litepolis_database_example import DatabaseActor
from fastapi import FastAPI, APIRouter, Depends
from fastapi.testclient import TestClient
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.authentication import requires
from litepolis_middleware_template.utils import verify_user_credentials
from litepolis_middleware_template.core import add_middleware, BasicAuth

class TestVerifyUserCredentials(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_user = DatabaseActor.create_user(email="alice@example.com", password="securepassword123")

    @classmethod
    def tearDownClass(cls):
        DatabaseActor.delete_user(cls.test_user.id)

    def test_correct_credentials(self):
        test_email = "alice@example.com"
        correct_password = "securepassword123"
        self.assertTrue(verify_user_credentials(test_email, correct_password))

    def test_incorrect_password(self):
        test_email = "alice@example.com"
        incorrect_password = "wrongpassword"
        self.assertFalse(verify_user_credentials(test_email, incorrect_password))

    def test_nonexistent_email(self):
        nonexistent_email = "nosuchuser@example.com"
        correct_password = "securepassword123"
        self.assertFalse(verify_user_credentials(nonexistent_email, correct_password))


class TestMiddlewareIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = FastAPI()
        cls.app = add_middleware(cls.app)

        @cls.app.get("/protected")
        @requires("authenticated")
        async def protected_route(request: Request):
            return JSONResponse({
                "message": "Hello, authenticated user!",
                "user": request.user.username
            })

        cls.client = TestClient(cls.app)
        cls.test_user = DatabaseActor.create_user(
            email="test_middleware@example.com",
            password="middlewarepassword"
        )

    @classmethod
    def tearDownClass(cls):
        DatabaseActor.delete_user(cls.test_user.id)

    def _get_auth_header(self, email, password):
        """Helper function to correctly create the Basic Auth header."""
        credentials_str = f"{email}:{password}"
        credentials_bytes = credentials_str.encode('utf-8')  # String to bytes
        base64_encoded_bytes = base64.b64encode(credentials_bytes) # Base64 encode bytes
        base64_encoded_str = base64_encoded_bytes.decode('ascii') # Base64 bytes to ASCII string
        return {'Authorization': 'Basic ' + base64_encoded_str}

    def test_valid_credentials_middleware(self):
        email = "test_middleware@example.com"
        password = "middlewarepassword"
        auth_header = self._get_auth_header(email, password)
        response = self.client.get("/protected", headers=auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Hello, authenticated user!")
        self.assertEqual(response.json()["user"], email)

    def test_invalid_credentials_middleware(self):
        email = "test_middleware@example.com"
        password = "wrongpassword"
        auth_header = self._get_auth_header(email, password)
        response = self.client.get("/protected", headers=auth_header)
        self.assertEqual(response.status_code, 400)

    def test_no_credentials_middleware(self):
        response = self.client.get("/protected")
        self.assertEqual(response.status_code, 403)