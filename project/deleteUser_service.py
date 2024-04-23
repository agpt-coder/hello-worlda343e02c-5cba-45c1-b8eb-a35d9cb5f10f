import prisma
import prisma.models
from pydantic import BaseModel


class DeleteUserResponse(BaseModel):
    """
    Response model indicating the result of the delete operation. It includes a success message or an error message in case of exceptions like user not found.
    """

    message: str
    deleted: bool


async def deleteUser(userId: int) -> DeleteUserResponse:
    """
    Deletes a specific user from the system using their UserID. This operation is usually
    restricted to user requests for account deletion or performed by an admin for managing
    user accounts.

    Args:
        userId (int): The unique identifier of the user to be deleted.

    Returns:
        DeleteUserResponse: Response model indicating the result of the delete operation.
                            It includes a success message or an error message in case of
                            exceptions like user not found.

    Example:
        deleteUser(1)
        > DeleteUserResponse(message="prisma.models.User deleted successfully", deleted=True)
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if user is None:
        return DeleteUserResponse(
            message=f"prisma.models.User with ID {userId} not found.", deleted=False
        )
    await prisma.models.Session.prisma().delete_many(where={"userId": userId})
    await prisma.models.APILog.prisma().delete_many(where={"userId": userId})
    await prisma.models.CLILog.prisma().delete_many(where={"userId": userId})
    await prisma.models.User.prisma().delete(where={"id": userId})
    return DeleteUserResponse(
        message="prisma.models.User deleted successfully", deleted=True
    )
