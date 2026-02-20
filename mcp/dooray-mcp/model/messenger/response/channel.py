from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Any
from model.types.deref_model import DerefModel
import json

class ChannelInfo(DerefModel):
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True, extra='ignore')

    id: str
    title: str
    type: Literal['direct', 'private', 'me', 'bot']
    # it has 'participants' (list[orgMember]).
    users: dict[str, list[Any]] | None = Field(exclude=True, default=None)
    role: Literal['admin', 'member', 'creator'] | None = None

    def model_dump_json(self, *args, **kwargs) -> str:
        d = super().model_dump(*args, **kwargs)
        if self.users is not None:
            d['participants'] = len(self.users['participants'])
        return json.dumps(d)