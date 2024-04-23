from datetime import datetime
from typing import List, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class Session(BaseModel):
    """
    Details about each session, including session IDs and timestamps.
    """

    id: int
    createdAt: datetime
    expiresAt: Optional[datetime] = None


class UserDetailsResponse(BaseModel):
    """
    Provides detailed information about a user including roles, email, and session details
    """

    id: int
    email: str
    role: prisma.enums.Role
    sessions: List[Session]


async def getUser(userId: int) -> UserDetailsResponse:
    """
    Retrieves a specific user's details by their unique identifier (UserID). The endpoint fetches user information and provides it in a secured manner. This is generally used by users to access their own information or by admins for auditing purposes.

    Args:
    userId (int): Unique identifier for the user. Used to fetch specific user details.

    Returns:
    UserDetailsResponse: Provides detailed information about a user including roles, email, and session details.
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"id": userId}, include={"sessions": True}
    )
    if user is None:
        raise Exception("User not found")
    sessions_details = [Session(**session.dict()) for session in user.sessions]
    user_details_response = UserDetailsResponse(
        id=user.id, email=user.email, role=user.role, sessions=sessions_details
    )
    return user_details_response
