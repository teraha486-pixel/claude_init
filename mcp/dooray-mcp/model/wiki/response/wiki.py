from model.types.deref_model import DerefModel
from model.projects.response.project import ProjectBrief
from pydantic import ConfigDict, Field

class Home(DerefModel):
    pageId: str

class WikiBrief(DerefModel):
    id: str
    name: str
    type: str
    project: ProjectBrief
    home: Home

class WikiPage(DerefModel):
    id: str
    subject: str
