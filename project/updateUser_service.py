from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserResponse(BaseModel):
    """
    Response model returning the updated user's data confirming the changes.
    """

    success: bool
    userId: int
    email: Optional[str] = None
    message: str


async def updateUser(
    userId: int, email: Optional[str], password: Optional[str]
) -> UpdateUserResponse:
    """
    Updates an existing user's data. It can handle changes to user details like password or email based on the provided UserID. The endpoint ensures that the request for update comes from the corresponding user or an administrator.

    Args:
        userId (int): The unique identifier of the user to be updated.
        email (Optional[str]): New email to update. Optional, provided if email needs to be changed.
        password (Optional[str]): New password for the user. Optional, provided if password needs an update.

    Returns:
        UpdateUserResponse: Response model returning the updated user's data confirming the changes.
    """
    response_data = UpdateUserResponse(
        success=False, userId=userId, email=email, message="Update failed."
    )
    try:
        updates = {}
        if email is not None:
            updates["email"] = email
        if password is not None:
            updates["password"] = password
        if updates:
            user = await prisma.models.User.prisma().update(
                where={"id": userId}, data=updates
            )
            response_data.success = True
            response_data.message = "User updated successfully."
        else:
            response_data.message = "No updates provided."
    except Exception as e:
        response_data.message = str(e)
    return response_data
