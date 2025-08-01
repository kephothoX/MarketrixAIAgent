from pydantic import BaseModel
from typing import List, Optional


class ImageData(BaseModel):
    """Model for image data with hash identifier.

    Attributes:
        serialized_image: Optional Base64 encoded string of the image content.
        mime_type: MIME type of the image.
    """

    serialized_image: str
    mime_type: str


class AgentResponse(BaseModel):
    """Model for a chat response.

    Attributes:
        response: The text response from the model.
        thinking_process: Optional thinking process of the model.
        attachments: List of image data to be displayed to the user.
        error: Optional error message if something went wrong.
    """

    response: str
    thinking_process: str = ""
    attachments: List[ImageData] = []
    error: Optional[str] = None


class AgentRequest(BaseModel):
    """Model for a chat request.

    Attributes:
        text: The text message to be sent to the model.
        files: List of image data to be sent to the model.
        session_id: Optional unique identifier for the chat session.
        user_id: Optional unique identifier for the user.
    """

    text: str
    files: List[ImageData] = []
