from model.types.deref_model import DerefModel
from typing import Any
from pydantic import Field, ConfigDict, BaseModel

class ApiHeader(DerefModel):
    isSuccessful: bool
    resultCode: int
    resultMessage: str | None = None

class ApiResponse(DerefModel):
    header: ApiHeader
    result: dict[str, Any] | list[dict[str, Any]] | None = None
    totalCount: int | None = None

class OrganizationMember(DerefModel):
    organizationMemberId: str 

class SimpleNameInfo(DerefModel):
    name: str

class SimpleIdInfo(DerefModel):
    id: str

class DoorayMemberDetailInfo(DerefModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: str = Field(description="Organization Member ID.")
    name: str = Field(description="Organization Member Name.")
    external_email_address: str | None = Field(default=None, alias="externalEmailAddress", description="External email address of the organization member.")
    nickname: str | None = Field(default=None, description="Nickname of the organization member.")
    default_organization: SimpleIdInfo | None = Field(default=None, alias="defaultOrganization", description="Default organization of the organization member.")