from app.models.assistant import Assistant
from app.dto.request.assistant_request import AssistantRequest
from app.dto.response.assistant_response import AssistantResponse
from typing import Optional


class AssistantMapper:
    @staticmethod
    def to_assistant(request: AssistantRequest) -> Optional[Assistant]:
        if request is None:
            return None

        return Assistant(
            code=request.code,
            name=request.name,
            about=request.about,
            temperature=request.temperature,
            imageUri=request.imageUri if request.imageUri else '',
            systemPrompt=request.systemPrompt,
            contextPrompt=request.contextPrompt,
            color=request.color,
            edgeVoice=request.edgeVoice,
            edgePitch=request.edgePitch,
            rvcVoice=request.rvcVoice
        )

    @staticmethod
    def to_assistant_response(assistant: Assistant):
        if assistant is None:
            return None

        return AssistantResponse(
            name=assistant.name,
            temperature=assistant.name,
            systemPrompt=assistant.name,
            contextPrompt=assistant.name,
            color=assistant.name,
            edgeVoice=assistant.name,
            edgePitch=assistant.name,
            rvcVoice=assistant.name,
            about=assistant.about,
            imageUri=assistant.imageUri
        )
