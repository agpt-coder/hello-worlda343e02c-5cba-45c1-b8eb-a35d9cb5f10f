import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class AuthTokenValidationResponse(BaseModel):
    """
    This model returns the result of the authentication token validation, indicating whether the operation was successful or not and what roles are permitted for subsequent requests.
    """

    success: bool
    message: str
    allowed_roles: List[str]


async def validateAuthToken(token: str) -> AuthTokenValidationResponse:
    """
    This endpoint validates authentication tokens to ensure that only authorized users can issue CLI commands.
    It receives a token via POST request, verifies it against stored credentials, and returns a JSON object
    indicating success or failure of authentication. This helps in maintaining secure access to CLI functionalities.

    Args:
    token (str): Authentication token provided by the client for validation.

    Returns:
    AuthTokenValidationResponse: This model returns the result of the authentication token validation,
    indicating whether the operation was successful or not and what roles are permitted for subsequent requests.
    """
    try:
        session_id = int(token)
    except ValueError:
        return AuthTokenValidationResponse(
            success=False, message="Invalid token format.", allowed_roles=[]
        )
    session = await prisma.models.Session.prisma().find_first(
        where={"id": session_id}, include={"user": True}
    )
    if (
        session
        and session.expiresAt
        and (session.expiresAt > datetime.datetime.utcnow())
    ):
        allowed_roles = [session.user.role] if session.user.role else []
        return AuthTokenValidationResponse(
            success=True,
            message="Token validated successfully.",
            allowed_roles=allowed_roles,
        )
    else:
        return AuthTokenValidationResponse(
            success=False, message="Invalid or expired token.", allowed_roles=[]
        )
