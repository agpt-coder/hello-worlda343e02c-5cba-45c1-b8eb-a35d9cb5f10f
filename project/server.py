import logging
from contextlib import asynccontextmanager
from typing import Optional

import prisma
import prisma.enums
import project.createUser_service
import project.deleteUser_service
import project.getHelloWorld_service
import project.getUser_service
import project.loginUser_service
import project.logoutUser_service
import project.processHelloWorldCommand_service
import project.updateUser_service
import project.validateAuthToken_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="hello-world",
    lifespan=lifespan,
    description="create a single hello world app",
)


@app.get(
    "/hello-world", response_model=project.getHelloWorld_service.HelloWorldResponse
)
async def api_get_getHelloWorld(
    request: project.getHelloWorld_service.HelloWorldRequest,
) -> project.getHelloWorld_service.HelloWorldResponse | Response:
    """
    This route handles GET requests at the '/hello-world' path. When accessed, it returns a 'Hello World' message. The route is straightforward and does not require any parameters or sophisticated logic. It cateres to public users and does not interface with other APIs or internal modules. Expected response is a simple text message saying 'Hello World'.
    """
    try:
        res = project.getHelloWorld_service.getHelloWorld(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/logout", response_model=project.logoutUser_service.LogoutResponseModel)
async def api_post_logoutUser(
    session_token: str,
) -> project.logoutUser_service.LogoutResponseModel | Response:
    """
    Manages user logout process. It invalidates the user's session token, ensuring that the session is closed on the server side, effectively logging the user out.
    """
    try:
        res = await project.logoutUser_service.logoutUser(session_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/users/{userId}", response_model=project.deleteUser_service.DeleteUserResponse
)
async def api_delete_deleteUser(
    userId: int,
) -> project.deleteUser_service.DeleteUserResponse | Response:
    """
    Deletes a specific user from the system using their UserID. This operation is usually restricted to user requests for account deletion or performed by an admin for managing user accounts.
    """
    try:
        res = await project.deleteUser_service.deleteUser(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/users", response_model=project.createUser_service.CreateUserResponse)
async def api_post_createUser(
    username: str, password: str, role: prisma.enums.Role
) -> project.createUser_service.CreateUserResponse | Response:
    """
    This route allows for the creation of a new user. It collects user data such as username and password, creates a new user record, and returns the user ID. The response will include a newly created user identifier (UserID). This action is typically utilized by administrators.
    """
    try:
        res = await project.createUser_service.createUser(username, password, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/cli/helloworld",
    response_model=project.processHelloWorldCommand_service.HelloWorldCommandResponse,
)
async def api_post_processHelloWorldCommand(
    token: str, command: str
) -> project.processHelloWorldCommand_service.HelloWorldCommandResponse | Response:
    """
    This endpoint processes the 'Hello World' command from the CLI. Upon validation of the user's token, it checks the command input. If the command is recognized, it responds with a 'Hello World' message in a JSON format. This allows the user to interact with the CLI in issuing specific commands and receiving appropriate feedback.
    """
    try:
        res = await project.processHelloWorldCommand_service.processHelloWorldCommand(
            token, command
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/users/{userId}", response_model=project.getUser_service.UserDetailsResponse)
async def api_get_getUser(
    userId: int,
) -> project.getUser_service.UserDetailsResponse | Response:
    """
    Retrieves a specific user's details by their unique identifier (UserID). The endpoint fetches user information and provides it in a secured manner. This is generally used by users to access their own information or by admins for auditing purposes.
    """
    try:
        res = await project.getUser_service.getUser(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/auth/validate",
    response_model=project.validateAuthToken_service.AuthTokenValidationResponse,
)
async def api_post_validateAuthToken(
    token: str,
) -> project.validateAuthToken_service.AuthTokenValidationResponse | Response:
    """
    This endpoint validates authentication tokens to ensure that only authorized users can issue CLI commands. It receives a token via POST request, verifies it against stored credentials, and returns a JSON object indicating success or failure of authentication. This helps in maintaining secure access to CLI functionalities.
    """
    try:
        res = await project.validateAuthToken_service.validateAuthToken(token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/login", response_model=project.loginUser_service.LoginResponse)
async def api_post_loginUser(
    username: str, password: str
) -> project.loginUser_service.LoginResponse | Response:
    """
    Handles user login request. Users provide credentials (username and password), and if validated correctly, the system returns an authentication token. This token is used for subsequent requests to verify the user's session.
    """
    try:
        res = await project.loginUser_service.loginUser(username, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/users/{userId}", response_model=project.updateUser_service.UpdateUserResponse
)
async def api_put_updateUser(
    userId: int, email: Optional[str], password: Optional[str]
) -> project.updateUser_service.UpdateUserResponse | Response:
    """
    Updates an existing user's data. It can handle changes to user details like password or email based on the provided UserID. The endpoint ensures that the request for update comes from the corresponding user or an administrator.
    """
    try:
        res = await project.updateUser_service.updateUser(userId, email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
