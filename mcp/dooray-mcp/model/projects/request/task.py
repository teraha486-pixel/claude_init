from pydantic import Field, ConfigDict
from typing import Optional, List, Literal
from model.dooray import OrganizationMember
from model.types.deref_model import DerefModel

class EmailUser(DerefModel):
    email_address: str = Field(alias="emailAddress", description="Email address of the external user.")
    name: str = Field(description="Name of the external user.")


class MemberRef(DerefModel):
    type: Literal["member", "emailUser"] = Field(description='Type of the user. Must be either "member" or "emailUser".')
    member: Optional[OrganizationMember] = Field(default=None, description="Organization member info. Required when type is 'member'.")
    email_user: Optional[EmailUser] = Field(default=None, alias="emailUser", description="Email user info. Required when type is 'emailUser'.")


class TaskBody(DerefModel):
    mime_type: Literal["text/html", "text/x-markdown"] = Field(alias="mimeType", description="MIME type of the content.", default="text/x-markdown")
    content: str = Field(description="Body content of the Task.", default="")


class TaskUsers(DerefModel):
    to: Optional[List[MemberRef]] = Field(default_factory=list, description="List of assignees for the Task.")
    cc: Optional[List[MemberRef]] = Field(default_factory=list, description="List of people to be CC'd on the Task.")


class CreateTask(DerefModel):
    subject: str = Field(description="Subject/title of the Task.")
    body: TaskBody = Field(description="Body of the Task.")

    parent_post_id: Optional[str] = Field(default=None, alias="parentTaskId", description="ID of the parent Task, if creating a subtask.")
    users: Optional[TaskUsers] = Field(default=None, description="Assignees and CCs for the Task.")
    due_date: Optional[str] = Field(default=None, alias="dueDate", description="Due date of the Task in ISO8601 format.")
    due_date_flag: Optional[bool] = Field(default=True, alias="dueDateFlag", description="(Deprecated) Use only with value `true`.")
    milestone_id: Optional[str] = Field(default=None, alias="milestoneId", description="Milestone ID associated with the Task.")
    tag_ids: Optional[List[str]] = Field(default_factory=list, alias="tagIds", description="List of tag IDs assigned to the Task.")
    priority: Optional[Literal["none", "highest", "high", "normal", "low", "lowest"]] = Field(
        default="none",
        description="Priority of the Task. Available values: 'none', 'highest', 'high', 'normal', 'low', 'lowest'."
    )

class ModifyTask(DerefModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    subject: str = Field(description="Subject/title of the Task. if user did not any mention, this field would be same with original task.")
    users: TaskUsers = Field(description="Assignees and CCs for the Task. if user did not any mention, this field would be same with original task.")
    body: TaskBody = Field(description="Body of the Task. if user did not any mention, this field would be same with original task.")
    due_date: Optional[str] = Field(default=None, alias="dueDate", description="Due date of the Task in ISO8601 format. if user did not any mention, this field would be same with original task.")
    due_date_flag: Optional[bool] = Field(default=True, alias="dueDateFlag", description="(Deprecated) Use only with value `true`. if user did not any mention, this field would be same with original task.")
    milestone_id: Optional[str] = Field(default=None, alias="milestoneId", description="Milestone ID associated with the Task. if user did not any mention, this field would be same with original task.")
    tag_ids: Optional[List[str]] = Field(default_factory=list, alias="tagIds", description="List of tag IDs assigned to the Task. if user did not any mention, this field would be same with original task.")
    priority: Literal["none", "highest", "high", "normal", "low", "lowest"] = Field(
        default="none",
        description="Priority of the Task. Available values: 'none', 'highest', 'high', 'normal', 'low', 'lowest'. if user did not any mention, this field would be same with original task."
    )
    version: str | None = Field(default=None, description="version of the task. always null.")
    
class TaskQueryParam(DerefModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    # 페이징 파라미터
    page: int = Field(default=0, description="Page number for pagination. Default is 0. 0-based index.")
    size: int = Field(default=100, ge=1, le=100, description="Page size for pagination. Default is 100, max is 100.")
    
    # 필터 파라미터
    from_email_address: str | None = Field(default=None, alias="fromEmailAddress", description="Filter tasks from a specific email address.")
    from_member_ids: str | None = Field(default=None, alias="fromMemberIds", description="Filter tasks from a specific organization member ID.")
    to_member_ids: str | None = Field(default=None, alias="toMemberIds", description="Filter tasks assigned to a specific organization member ID.")
    cc_member_ids: str | None = Field(default=None, alias="ccMemberIds", description="Filter tasks CC'd to a specific organization member ID.")
    tag_ids: str | None = Field(default=None, alias="tagIds", description="Filter tasks with a specific tag IDs. the condition of ids that was seperated by comma is 'and' condition", pattern="(\\d+)(,(\\d+))*")
    parent_post_id: str | None = Field(default=None, alias="parentPostId", description="Filter subtasks of a specific parent task id.")
    post_number: str | None = Field(default=None, alias="postNumber", description="Filter task by its identity number.")
    post_workflow_classes: str | None = Field(default=None, alias="postWorkflowClasses", pattern="((backlog|registered|working|closed),)*(backlog|registered|working|closed)",  # 정규 표현식으로 필터링
                                              description="""
                                              Filter tasks by workflow class. Available values: backlog, registered, working, closed.
                                              the condition of classes that was seperated by comma is 'or' condition.

                                              backlog(syn. waiting): Task was created but not yet registered. it is waiting for review or examination to be registered.
                                              registered(syn. todo): Task was registered so that it can be worked on. but not yet started by assignees.
                                              working(syn. proceeding): Task is currently being worked on by assignees.
                                              closed(syn. completed): Task is completed and closed.
                                              """
                                              )
    post_workflow_ids: str | None = Field(default=None, alias="postWorkflowIds", description="Filter tasks by workflow ID defined in the project. the condition of ids that was seperated by comma is 'or' condition", pattern="(\\d+)(,(\\d+))*")
    milestone_ids: str | None = Field(default=None, alias="milestoneIds", description="Filter tasks by milestone IDs.", pattern="(\\d+)(,(\\d+))*")
    subjects: str | None = Field(default=None, alias="subjects", description="Filter tasks by title/subject.")
    
    # 시간 기반 필터 파라미터
    created_at: str | None = Field(default=None, alias="createdAt", description="Filter tasks by creation time. Formats: today, thisweek, prev-{N}d, next-{N}d, or ISO8601 range.")
    updated_at: str | None = Field(default=None, alias="updatedAt", description="Filter tasks by update time. Formats: today, thisweek, prev-{N}d, next-{N}d, or ISO8601 range.")
    due_at: str | None = Field(default=None, alias="dueAt", description="Filter tasks by due date. Formats: today, thisweek, prev-{N}d, next-{N}d, or ISO8601 range.")
    
    # 정렬 파라미터
    order: str | None = Field(default=None, description="Sort order. Available values: postDueAt, postUpdatedAt, createdAt. Prefix with '-' for descending order.(e.g. '-createdAt')")