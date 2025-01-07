from objectbox import Id, Entity, String, Float32, Int8

@Entity()
class Assistant:
    id=Id()
    code= String()
    name = String()
    about = String()
    temperature =  Float32()
    imageUri = String()
    systemPrompt = String(),
    contextPrompt = String()
    color = String()
    edgeVoice = String()
    edgePitch = Int8()
    rvcVoice = String()