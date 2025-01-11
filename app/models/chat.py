from objectbox import Int64, Entity, Id, String, Bool
from app.models.base_model import BaseModel

@Entity()
class Chat(BaseModel):
    id = Id()
    code = String()
    type = String()
    password = String()
    name = String()
    imageUri = String()
    showSystemMessages = Bool()
    showFailedMessages = Bool()
    showCommands = Bool()
    showTokens = Bool()
    autoPlaybackAudio= Bool()
    autoResponses = Bool()
    ownerUserCode = String()

    #Other relations
    assistant_id = Int64
    user_id = Int64
