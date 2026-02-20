from model.types.deref_model import DerefModel
from model.projects.response.project import ProjectBrief
from pydantic import Field
from typing import Literal
from model.dooray import SimpleNameInfo, SimpleIdInfo, OrganizationMember

class TaskInfo(DerefModel):
    id: str
    subject: str
    number: int
    closed: bool
    priority: str
    project: ProjectBrief
    worlflow_class: Literal['backlog', 'registered', 'working', 'closed'] = Field(alias="workflowClass", description="Workflow class of the task.")
    workflow: SimpleNameInfo = Field(description="Workflow information of the task.")
    milestone: SimpleNameInfo | None = Field(default=None, description="Milestone information of the task. null if not in a milestone.")
    tags: list[SimpleIdInfo] = Field(default_factory=list, description="List of tag IDs assigned to the task.")


class TaskBody(DerefModel):
    mimeType: str
    content: str

class TaskDetail(DerefModel):
    id: str
    subject: str
    number: int
    closed: bool
    priority: str
    project: ProjectBrief
    body: TaskBody


# ============ 상세 조회용 타입 (Full Detail) ============

class WorkflowInfo(DerefModel):
    """워크플로우 정보"""
    id: str
    name: str

class MemberInfo(DerefModel):
    """멤버 정보"""
    organizationMemberId: str
    name: str

class GroupMemberInfo(DerefModel):
    """그룹 내 멤버 정보"""
    organizationMemberId: str
    name: str

class GroupInfo(DerefModel):
    """그룹 정보"""
    projectMemberGroupId: str
    code: str
    members: list[GroupMemberInfo] = Field(default_factory=list)

class TaskUserFrom(DerefModel):
    """등록자 정보"""
    type: str
    member: MemberInfo | None = None

class TaskUserTo(DerefModel):
    """담당자 정보"""
    type: str
    member: MemberInfo | None = None
    workflow: WorkflowInfo | None = None

class TaskUsers(DerefModel):
    """업무 사용자 정보 (등록자, 담당자, 참조)"""
    from_: TaskUserFrom | None = Field(default=None, alias="from")
    to: list[TaskUserTo] = Field(default_factory=list)
    cc: list[dict] = Field(default_factory=list, description="참조자 목록 (member 또는 group)")

class FileInfo(DerefModel):
    """첨부파일 정보"""
    id: str
    name: str
    size: int | None = None
    mimeType: str | None = None
    createdAt: str | None = None

class MilestoneFullInfo(DerefModel):
    """마일스톤 정보"""
    id: str
    name: str

class TagIdInfo(DerefModel):
    """태그 ID 정보"""
    id: str

class TaskFullDetail(DerefModel):
    """업무 전체 상세 정보 (모든 필드 포함)"""
    id: str
    subject: str
    number: int
    closed: bool
    priority: str
    project: ProjectBrief
    body: TaskBody

    # 워크플로우 정보
    workflowClass: Literal['backlog', 'registered', 'working', 'closed'] | None = Field(
        default=None,
        description="워크플로우 클래스 (backlog: 대기, registered: 등록, working: 진행중, closed: 완료)"
    )
    workflow: WorkflowInfo | None = Field(default=None, description="워크플로우 정보")

    # 마일스톤/태그
    milestone: MilestoneFullInfo | None = Field(default=None, description="마일스톤 정보")
    tags: list[TagIdInfo] = Field(default_factory=list, description="태그 ID 목록")

    # 사용자 정보
    users: TaskUsers | None = Field(default=None, description="등록자, 담당자, 참조자 정보")

    # 날짜 정보
    dueDate: str | None = Field(default=None, description="만기일")
    dueDateFlag: bool | None = Field(default=None, description="만기일 사용 여부")
    createdAt: str | None = Field(default=None, description="생성일")
    updatedAt: str | None = Field(default=None, description="수정일")

    # 상위 업무
    parentPost: dict | None = Field(default=None, description="상위 업무 정보")

    # 첨부파일
    files: list[FileInfo] = Field(default_factory=list, description="첨부파일 목록")
