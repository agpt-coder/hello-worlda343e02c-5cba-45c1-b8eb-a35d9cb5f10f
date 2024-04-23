from datetime import datetime, timedelta

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class LoginResponse(BaseModel):
    """
    The response returned upon a successful login. It includes an authentication token for session management.
    """

    auth_token: str


async def loginUser(username: str, password: str) -> LoginResponse:
    """
    Handles user login request. Users provide credentials (username and password), and if validated correctly, the system returns an authentication token. This token is used for subsequent requests to verify the user's session.

    Args:
        username (str): The username input by the user, used to identify their account.
        password (str): The password input by the user, used for authentication.

    Returns:
        LoginResponse: The response returned upon a successful login. It includes an authentication token for session management.

    """
    user = await prisma.models.User.prisma().find_unique(where={"email": username})
    if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        new_session = await prisma.models.Session.prisma().create(
            data={"userId": user.id, "expiresAt": datetime.now() + timedelta(days=1)}
        )
        auth_token = f"token-{new_session.id}"
        return LoginResponse(auth_token=auth_token)
    else:
        raise Exception("Invalid username or password")
