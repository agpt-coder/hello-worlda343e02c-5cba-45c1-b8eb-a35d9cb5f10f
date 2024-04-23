import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class HelloWorldCommandResponse(BaseModel):
    """
    Model for the response of a 'Hello World' command in the CLI module, confirming the command was received and processed.
    """

    message: str


async def processHelloWorldCommand(
    token: str, command: str
) -> HelloWorldCommandResponse:
    """
    This endpoint processes the 'Hello World' command from the CLI. Upon validation of the user's token, it checks the command input. If the command is recognized, it responds with a 'Hello World' message in a JSON format. This allows the user to interact with the CLI in issuing specific commands and receiving appropriate feedback.

    Args:
        token (str): Access token for user validation.
        command (str): The CLI command issued by the user.

    Returns:
        HelloWorldCommandResponse: Model for the response of a 'Hello World' command in the CLI module, confirming the command was received and processed.

    Example:
        token = '123'
        command = 'hello'
        response = await processHelloWorldCommand(token, command)
        print(response)
        > HelloWorldCommandResponse(message='Hello World')
    """
    session = await prisma.models.Session.prisma().find_unique(where={"id": int(token)})
    if not session or (
        session.expiresAt and session.expiresAt < datetime.datetime.now()
    ):
        return HelloWorldCommandResponse(message="Invalid or expired token.")
    await prisma.models.CLILog.prisma().create(
        data={
            "userId": session.userId,
            "command": command,
            "executedAt": datetime.datetime.now(),
        }
    )
    if command == "hello":
        message = "Hello World"
    else:
        message = "Command not recognized"
    return HelloWorldCommandResponse(message=message)
