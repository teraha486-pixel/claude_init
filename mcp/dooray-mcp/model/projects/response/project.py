from model.types.deref_model import DerefModel
from typing import Literal
from pydantic import ConfigDict, Field

class ProjectBrief(DerefModel):
    id: str

class ProjectInfo(DerefModel):
    id: str
    code: str
    description: str
    scope: str
    type: str

class MilestoneInfo(DerefModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: str = Field(description="Milestone ID.")
    name: str = Field(description="Milestone name.")
    status: Literal['open', 'closed'] = Field(description="Milestone status. 'open' or 'closed'.")
    started_at: str = Field(alias="startedAt", description="Milestone start date.")
    ended_at: str = Field(alias="endedAt", description="Milestone end date.")
    closed_at: str | None = Field(default=None, alias="closedAt", description="Milestone closed date. null if not closed.")

class TagGroupInfo(DerefModel):
    id: str = Field(description="Tag group ID.")
    name: str = Field(description="Tag group name.")
    mandatory: bool = Field(description="Is this tag group mandatory? true or false.")
    selectOne: bool = Field(description="Is this tag group single select? true or false.")

class TagInfo(DerefModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: str = Field(description="Tag ID.")
    name: str = Field(description="Tag name.")
    tag_group: TagGroupInfo | None = Field(default=None, alias="tagGroup", description="Tag group information. null if not in a tag group.")
