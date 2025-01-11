from app.models.chat import Chat
from app.dto.request.chat_request import ChatRequest
from app.dto.response.chat_response import ChatResponse
from typing import Optional


class ChatMapper:
    @staticmethod
    def to_chat(request: ChatRequest) -> Optional[Chat]:
        if request is None:
            return None

        return Chat(
            code=request.code,
            password=request.password,
            name=request.name,
            imageUri=request.imageUri,
            showSystemMessages=request.showSystemMessages,
            showFailedMessages=request.showFailedMessages,
            showCommands=request.showCommands,
            showTokens=request.showTokens,
            autoPlaybackAudio=request.autoPlaybackAudio,
            autoResponses=request.autoResponses,
            ownerUserCode=request.ownerUserCode,
            assistant_id=request.assistant_id,
            user_id=request.user_id
        )

    @staticmethod
    def to_chat_response(chat: Chat):
        if chat is None:
            return None

        return ChatResponse(
            name=chat.name,
            type=chat.type,
            imageUri=chat.imageUri
        )
