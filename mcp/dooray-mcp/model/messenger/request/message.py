from pydantic import Field, ConfigDict
from model.types.deref_model import DerefModel

class DirectMessage(DerefModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    text: str = Field(description='a message to send to opponent')
    organization_member_id: str = Field(alias='organizationMemberId', description='member id in organization')

class Message(DerefModel):
    text: str = Field(description='a message to send')