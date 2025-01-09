from enum import Enum

class MessageSenderType(str, Enum):
    ASSISTANT = "assistant"
    USER = "user"
    SYSTEM = "system"
    SELF = "self"

class MessageType(Enum):
    TEXT = ("text", "text/plain")
    AUDIO = ("audio", "audio/*")
    VIDEO = ("video", "video/*")
    IMAGE = ("image", "image/*")
    DOCUMENT = ("document", "application/*")

    def __init__(self, value: str, mime_type: str):
        self.value = value
        self.mime_type = mime_type