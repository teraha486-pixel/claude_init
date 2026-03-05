import httpx
import server
import mcp.types as types
from adapter.projects import task
from model.projects.request.task import CreateTask, ModifyTask, TaskQueryParam
from model.projects.response.task import TaskInfo
from utils import converter

@server.register_tool(
    description="""
    search task list with assignee or cc member id..
    there must be a member id at least among these two assignee or cc to search task list.
    if my member id is needed, please use get_my_member_identities tool.
    """,
    inputSchema={
        "type": "object",
        "properties": {
            "project_id": {
                "type": "array",
                "description":
                """
                target project id list to search task list.
                """,
                "items": {
                    "type": "string"
                }
            },
            "assignee": {
                "type": "string",
                "description":
                """
                assignee member id to search task list.
                """
            },
            "cc": {
                "type": "string",
                "description":
                """
                cc member id to search task list.
                """
            },
            # "task_query": TaskSearchParam.model_json_schema(),
        },
        "required": ["project_id"]
    }
)
async def get_task_list_by_assignee_or_cc(project_id: list[str], assignee: str | None = None, cc: str | None = None):
    response: list[TaskInfo] = await task.get_task_list_by_assignee_cc(project_id, assignee, cc) 
    return converter.convert_mcp_text_output(response)

@server.register_tool(
    description="""
    search task list with task query.
    if you want to search task list with params such as milestone, status, etc, use this tool.
    this tool searches task list once by one project id unlike get_task_list_by_assignee_or_cc tool.
    please use multiple times if you want to search task list with multiple project ids.
    """,
    inputSchema={
        "type": "object",
        "properties": {
            "project_id": {
                "type": "string",
                "description":
                """
                target project id to search task list.
                """
            },
            "task_query": TaskQueryParam.model_json_schema(),
        },
        "required": ["project_id", "task_query"]
    }
)
async def get_task_list_with_param(project_id: str, task_query: dict):
    response: list[TaskInfo] = await task.get_task_list_with_param(project_id, TaskQueryParam(**task_query))
    return converter.convert_mcp_text_output(response)

@server.register_tool(
    description="""
    Get task detail.

    before using modify_task tool, you must call the this tool.
    """,
    inputSchema={
        "type": "object",
        "properties": {
            "project_id": {
                "type": "string",
                "description":
                """
                project id that target task belongs to.
                """
            },
            "post_id": {
                "type": "string",
                "description": 
                """
                target post id
                """
            }
        },
        "required": ["project_id", "post_id"]
    }
)
async def get_detail_of_task(project_id: str, post_id: str):
    response = await task.get_detail_of_task(project_id, post_id)
    return converter.convert_mcp_text_output(response)

@server.register_tool(
    description="""
    Get task detail by post_id only.

    Use this tool when you have a Dooray task URL like https://nhnent.dooray.com/project/tasks/1234567890
    You can extract the post_id (1234567890) from the URL and query directly without knowing the project_id.

    This is useful when user provides a Dooray task link.
    """,
    inputSchema={
        "type": "object",
        "properties": {
            "post_id": {
                "type": "string",
                "description":
                """
                task id extracted from Dooray URL.
                Example: from https://nhnent.dooray.com/project/tasks/1234567890123456789, use 1234567890123456789
                """
            }
        },
        "required": ["post_id"]
    }
)
async def get_detail_of_task_by_id(post_id: str):
    response = await task.get_detail_of_task_by_id(post_id)
    return converter.convert_mcp_text_output(response)

# ============ 업무 전체 상세 조회 (Full Detail) ============

@server.register_tool(
    description="""
    업무의 전체 상세 정보를 조회합니다.
    워크플로우 상태, 등록자, 담당자, 참조자, 태그, 마일스톤, 만기일, 첨부파일, 생성일, 수정일 등 모든 정보를 포함합니다.

    일반 get_detail_of_task보다 더 상세한 정보가 필요할 때 사용하세요.
    """,
    inputSchema={
        "type": "object",
        "properties": {
            "project_id": {
                "type": "string",
                "description": "프로젝트 ID"
            },
            "post_id": {
                "type": "string",
                "description": "업무 ID"
            }
        },
        "required": ["project_id", "post_id"]
    }
)
async def get_full_detail_of_task(project_id: str, post_id: str):
    response = await task.get_full_detail_of_task(project_id, post_id)
    return converter.convert_mcp_text_output(response)

@server.register_tool(
    description="""
    post_id만으로 업무의 전체 상세 정보를 조회합니다.
    워크플로우 상태, 등록자, 담당자, 참조자, 태그, 마일스톤, 만기일, 첨부파일, 생성일, 수정일 등 모든 정보를 포함합니다.

    두레이 업무 URL (예: https://nhnent.dooray.com/project/tasks/1234567890123456789)에서
    업무 ID(1234567890123456789)를 추출하여 사용할 수 있습니다.

    일반 get_detail_of_task_by_id보다 더 상세한 정보가 필요할 때 사용하세요.
    """,
    inputSchema={
        "type": "object",
        "properties": {
            "post_id": {
                "type": "string",
                "description": "업무 ID (두레이 URL에서 추출)"
            }
        },
        "required": ["post_id"]
    }
)
async def get_full_detail_of_task_by_id(post_id: str):
    response = await task.get_full_detail_of_task_by_id(post_id)
    return converter.convert_mcp_text_output(response)

@server.register_tool(
    description="dooray task creater. and it is part of task(project).",
    inputSchema={
        "type": "object",
        "properties": {
            "request": CreateTask.model_json_schema(),
            "project_id": {
                "type": "string",
                "description": 
                """
                target project id
                """
            }
        },
        "required": ["request", "project_id"]
    }
)
async def create_task(request: dict, project_id:str):
    response: httpx.Response = await task.create_task(request, project_id)
    return [types.TextContent(type="text", text=response.text)]

@server.register_tool(
    description="""
    upload file to dooray task.

    if you want to post a image into content of task, you must upload that image first using upload_file_to_task tool.
    and then, make a path to that image with given id as result of upload_file_to_task tool.
    task image url format is like this:
    ![](/files/{id}) or html tag like this <img src="/files/{id}" />

    and then, modify the task page content with that markdown image format..
    """,
    inputSchema={
        "type": "object",
        "properties": {
            "project_id": {
                "type": "string",
                "description": 
                """
                target project id
                """
            },
            "post_id": {
                "type": "string",
                "description": 
                """
                target task id where file will be uploaded
                """
            },
            "file_path": {
                "type": "string",
                "description": 
                """
                target file path
                """
            },
        },
        "required": ["project_id", "post_id", "file_path"]
    }
)
async def upload_file_to_task(project_id: str, post_id: str, file_path: str):
    response: str = await task.upload_file_to_task(project_id, post_id, file_path)
    return [types.TextContent(type="text", text=response)]

@server.register_tool(
    description="""
    modify task.

    before using this tool, you must call the get_detail_of_task tool.

    if you want to post a image into content of task, you must upload that image first using upload_file_to_task tool.
    and then, make a path to that image with given id as result of upload_file_to_task tool.
    task image url format is like this:
    ![](/files/{id}) or html tag like this <img src="/files/{id}" />

    and then, modify the task body content with that markdown image format..
    """,
    inputSchema={
        "type": "object",
        "properties": {
            "project_id": {
                "type": "string",
                "description": 
                """
                target project id
                """
            },
            "post_id": {
                "type": "string",
                "description": 
                """
                target task id to modify
                """
            },
            "modify": ModifyTask.model_json_schema()
        },
        "required": ["project_id", "post_id", "modify"]
    }
)
async def modify_task(project_id: str, post_id: str, modify: dict) -> list[types.TextContent]:
    response: httpx.Response = await task.modify_task(project_id, post_id, ModifyTask(**modify))
    return [types.TextContent(type="text", text=response.text)]

# ============ 업무 상태 변경 관련 도구 ============

@server.register_tool(
    description="두레이 프로젝트 업무의 상태(워크플로우)를 변경합니다. 업무 전체의 상태를 변경하며, 모든 담당자의 상태가 함께 변경됩니다.",
    inputSchema={
        "type": "object",
        "properties": {
            "project_id": {
                "type": "string",
                "description": "프로젝트 ID"
            },
            "post_id": {
                "type": "string",
                "description": "업무 ID"
            },
            "workflow_id": {
                "type": "string",
                "description": "변경할 워크플로우 ID"
            }
        },
        "required": ["project_id", "post_id", "workflow_id"]
    }
)
async def set_post_workflow(project_id: str, post_id: str, workflow_id: str) -> list[types.TextContent]:
    response: httpx.Response = await task.set_post_workflow(project_id, post_id, workflow_id)
    return [types.TextContent(type="text", text=response.text)]

@server.register_tool(
    description="두레이 프로젝트 업무를 완료 상태로 변경합니다. 완료 클래스 내의 대표 상태로 변경되며, 모든 담당자의 상태가 완료로 변경됩니다.",
    inputSchema={
        "type": "object",
        "properties": {
            "project_id": {
                "type": "string",
                "description": "프로젝트 ID"
            },
            "post_id": {
                "type": "string",
                "description": "업무 ID"
            }
        },
        "required": ["project_id", "post_id"]
    }
)
async def set_post_done(project_id: str, post_id: str) -> list[types.TextContent]:
    response: httpx.Response = await task.set_post_done(project_id, post_id)
    return [types.TextContent(type="text", text=response.text)]

# ============ 업무 댓글 관련 도구 ============

@server.register_tool(
    description="두레이 프로젝트 업무의 댓글 목록을 조회합니다. 페이징과 정렬 옵션을 지원합니다.",
    inputSchema={
        "type": "object",
        "properties": {
            "project_id": {
                "type": "string",
                "description": "프로젝트 ID"
            },
            "post_id": {
                "type": "string",
                "description": "업무 ID"
            },
            "page": {
                "type": "integer",
                "description": "페이지 번호 (0부터 시작, 기본값: 0)",
                "default": 0
            },
            "size": {
                "type": "integer",
                "description": "페이지 크기 (최대 100, 기본값: 20)",
                "default": 20
            },
            "order": {
                "type": "string",
                "description": "정렬 조건 (createdAt: 오래된순, -createdAt: 최신순, 기본값: createdAt)",
                "default": "createdAt"
            }
        },
        "required": ["project_id", "post_id"]
    }
)
async def get_post_comments(project_id: str, post_id: str, page: int = 0, size: int = 20, order: str = "createdAt") -> list[types.TextContent]:
    response: httpx.Response = await task.get_post_comments(project_id, post_id, page, size, order)
    return [types.TextContent(type="text", text=response.text)]

@server.register_tool(
    description="두레이 프로젝트 업무에 댓글을 생성합니다. 마크다운 또는 HTML 형식으로 댓글을 작성할 수 있습니다.",
    inputSchema={
        "type": "object",
        "properties": {
            "project_id": {
                "type": "string",
                "description": "프로젝트 ID"
            },
            "post_id": {
                "type": "string",
                "description": "업무 ID"
            },
            "content": {
                "type": "string",
                "description": "댓글 내용"
            },
            "mime_type": {
                "type": "string",
                "description": "MIME 타입 (text/x-markdown 또는 text/html, 기본값: text/x-markdown)",
                "default": "text/x-markdown"
            }
        },
        "required": ["project_id", "post_id", "content"]
    }
)
async def create_post_comment(project_id: str, post_id: str, content: str, mime_type: str = "text/x-markdown") -> list[types.TextContent]:
    response: httpx.Response = await task.create_post_comment(project_id, post_id, content, mime_type)
    return [types.TextContent(type="text", text=response.text)]

@server.register_tool(
    description="두레이 프로젝트 업무의 댓글을 수정합니다. 이메일로 발송된 댓글은 수정할 수 없습니다.",
    inputSchema={
        "type": "object",
        "properties": {
            "project_id": {
                "type": "string",
                "description": "프로젝트 ID"
            },
            "post_id": {
                "type": "string",
                "description": "업무 ID"
            },
            "log_id": {
                "type": "string",
                "description": "댓글 ID (get_post_comments로 조회 가능)"
            },
            "content": {
                "type": "string",
                "description": "수정할 댓글 내용"
            },
            "mime_type": {
                "type": "string",
                "description": "MIME 타입 (text/x-markdown 또는 text/html, 기본값: text/x-markdown)",
                "default": "text/x-markdown"
            }
        },
        "required": ["project_id", "post_id", "log_id", "content"]
    }
)
async def update_post_comment(project_id: str, post_id: str, log_id: str, content: str, mime_type: str = "text/x-markdown") -> list[types.TextContent]:
    response: httpx.Response = await task.update_post_comment(project_id, post_id, log_id, content, mime_type)
    return [types.TextContent(type="text", text=response.text)]

@server.register_tool(
    description="두레이 프로젝트 업무의 댓글을 삭제합니다.",
    inputSchema={
        "type": "object",
        "properties": {
            "project_id": {
                "type": "string",
                "description": "프로젝트 ID"
            },
            "post_id": {
                "type": "string",
                "description": "업무 ID"
            },
            "log_id": {
                "type": "string",
                "description": "삭제할 댓글 ID (get_post_comments로 조회 가능)"
            }
        },
        "required": ["project_id", "post_id", "log_id"]
    }
)
async def delete_post_comment(project_id: str, post_id: str, log_id: str) -> list[types.TextContent]:
    response: httpx.Response = await task.delete_post_comment(project_id, post_id, log_id)
    return [types.TextContent(type="text", text=response.text)]