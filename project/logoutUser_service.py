import prisma
import prisma.models
from pydantic import BaseModel


class LogoutResponseModel(BaseModel):
    """
    This model returns the status of the logout operation to inform the client whether the session was successfully closed.
    """

    logout_success: bool
    message: str


async def logoutUser(session_token: str) -> LogoutResponseModel:
    """
    Manages user logout process. It invalidates the user's session token, ensuring that the session is closed on the server side, effectively logging the user out.

    Args:
        session_token (str): The token that uniquely identifies the user session to be invalidated.

    Returns:
        LogoutResponseModel: This model returns the status of the logout operation to inform the client whether the session was successfully closed.
    """
    try:
        session = await prisma.models.Session.prisma().find_unique(
            where={"id": session_token}
        )
        if session is None:
            return LogoutResponseModel(
                logout_success=False, message="Session not found"
            )
        await prisma.models.Session.prisma().delete(where={"id": session_token})
        return LogoutResponseModel(
            logout_success=True, message="Successfully logged out."
        )
    except Exception as e:
        return LogoutResponseModel(
            logout_success=False, message=f"Logout failed: {str(e)}"
        )
