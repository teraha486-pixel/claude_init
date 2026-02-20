from model.types.deref_model import DerefModel
from model.projects.response.project import ProjectBrief

class DriveBrief(DerefModel):
    id: str
    name: str
    type: str
    project: ProjectBrief

class DriveInfo(DerefModel):
    id: str
    name: str
    type: str
    hasFolders: bool
    mimeType: str
    subType: str