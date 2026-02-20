from model.types.deref_model import DerefModel
from pydantic import Field, ConfigDict
from model.dooray import OrganizationMember

class WikiBody(DerefModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    mime_type: str = Field(alias='mimeType', description='text/x-markdown', default='text/x-markdown')
    content: str = Field(description='content of wiki', default='')

class Referrer(DerefModel):
    type: str = Field(description='member or department')
    member: OrganizationMember = Field(description='member or department id to be referenced this wiki page')

class CreateWiki(DerefModel):
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    parent_page_id: str = Field(alias='parentPageId', description='parent wiki page id where new wiki page would be added.')
    subject: str = Field(description='subject of wiki page. required.')
    body: WikiBody = Field(description='body of wiki. required.')
    attach_file_ids: list[str] = Field(description='attach file id list to be attached in wiki. default value is empty list', default=[])
    referrers: list[Referrer] = Field(description='list of referrer. default value is empty list')

class WikiModifyBody(DerefModel):
    body: WikiBody = Field(description='body of wiki', default=WikiBody())

    @classmethod
    def from_content(cls, content: str) -> 'WikiModifyBody':
        return cls(body=WikiBody(content=content))
