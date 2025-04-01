import base64
import binascii

from starlette.authentication import (AuthenticationBackend,
                                      AuthenticationError,
                                      SimpleUser,
                                      AuthCredentials)
from starlette.middleware.authentication import AuthenticationMiddleware
from litepolis_database_example import DatabaseActor

from .utils import verify_user_credentials

class BasicAuth(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return None

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise AuthenticationError("Invalid basic auth credentials")

        email, _, password = decoded.partition(":")
        database_actor = DatabaseActor() # Instantiate DatabaseActor
        user = verify_user_credentials(email, password) # Use DatabaseActor to verify user, assuming username is used
        if user is not True:
            raise AuthenticationError("Invalid user or password")
        return AuthCredentials(["authenticated"]), SimpleUser(email)


def add_middleware(app):
    app.add_middleware(AuthenticationMiddleware, backend=BasicAuth())
    return app
