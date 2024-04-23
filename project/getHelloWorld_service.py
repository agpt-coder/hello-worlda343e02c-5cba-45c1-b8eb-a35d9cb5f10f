from pydantic import BaseModel


class HelloWorldRequest(BaseModel):
    """
    A simple request model for the '/hello-world' endpoint. This model does not require any fields because the endpoint does not accept any parameters.
    """

    pass


class HelloWorldResponse(BaseModel):
    """
    Response model for the '/hello-world' endpoint, providing a basic string message as output.
    """

    message: str


def getHelloWorld(request: HelloWorldRequest) -> HelloWorldResponse:
    """
    This route handles GET requests at the '/hello-world' path. When accessed, it returns a 'Hello World' message. The route is straightforward and does not require any parameters or sophisticated logic. It caters to public users and does not interface with other APIs or internal modules. Expected response is a simple text message saying 'Hello World'.

    Args:
        request (HelloWorldRequest): A simple request model for the '/hello-world' endpoint. This model does not require any fields because the endpoint does not accept any parameters.

    Returns:
        HelloWorldResponse: Response model for the '/hello-world' endpoint, providing a basic string message as output.
    """
    return HelloWorldResponse(message="Hello World")
