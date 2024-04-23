from enum import Enum

import prisma
import prisma.models
from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    """
    This model represents the response payload after creating a new user. It includes the user ID of the newly created user.
    """

    userId: int


class Role(Enum):
    Admin: str = "Admin"
    User: str = "User"


async def createUser(username: str, password: str, role: Role) -> CreateUserResponse:
    """
    This route allows for the creation of a new user. It collects user data such as username and password, creates a new user record, and returns the user ID. The response will include a newly created user identifier (UserID). This action is typically utilized by administrators.

    Args:
        username (str): The username for the new user account. Must be unique across all users.
        password (str): The password for securing the new user account.
        role (Role): The role assigned to the user which determines their access permissions.

    Returns:
        CreateUserResponse: This model represents the response payload after creating a new user. It includes the user ID of the newly created user.

    Example:
        createUser("john.doe@example.com", "securepassword123", Role.Admin)
        > CreateUserResponse(userId=1)
    """
    new_user = await prisma.models.User.prisma().create(
        data={"email": username, "password": password, "role": role.value}
    )
    return CreateUserResponse(userId=new_user.id)
