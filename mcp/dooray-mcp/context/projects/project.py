from model.projects.response.project import ProjectInfo, TagInfo, MilestoneInfo
import server
import mcp.types as types
from adapter.projects import project
from utils import converter;

@server.register_tool(
    description = "get task list which is able to access.",
    inputSchema={
        "type": "object",
        "properties": {
            "page": {
                "type": "integer",
                "description": 
                """
                page number(0 base), Default value : 0
                """
            },
            "size": {
                "type": "integer",
                "description": 
                """
                page size, Default value : 100, max value: 100
                """
            },
            "project_type": {
                "type": "string",
                "description": 
                """
                type of project. Literal value is 'public'.
                default value is 'public'.

                'public' : public project

                
                """
                # 개인 프로젝트를 찾을 때는 private 를 사용해야 하는데, 아래와 같은 description 을 사용했지만, 
                # ai 가 용어를 이해하기 힘든지, '나의' 만 들어가면 무조건 private 을 사용하여 public 만 찾도록 주석처리.
                # +"""'private' : personal project
                # if the user wants to get a `personal private`(not `my`) project, try with 'private'."""
            }
        },
        "required": ["page", "size", "project_type"]
    }
)
async def get_my_project_list(page: int, size: int, project_type: str='public') -> list[types.TextContent]:
    response: list[ProjectInfo] = await project.get_my_project_list(page=page, size=size, project_type=project_type)
    return converter.convert_mcp_text_output(response)
    
@server.register_tool(
    description="""
    get project milestones.
    it is used for getting milestone(syn. step, phase, ...) list of project.
    """,
    inputSchema={
        "type": "object",
        "properties": {
            "project_id": {
                "type": "string",
                "description":
                """
                target project id to get milestone list.
                """
            },
            "page": {
                "type": "integer",
                "description":
                """
                page number(0 base), Default value : 0
                """
            },
            "size": {
                "type": "integer",
                "description":
                """
                page size, Default value : 100, max value: 100
                """
            },
            "status": {
                "type": "string",
                "description":
                """
                status of milestone. available values are 'open', 'closed'.
                """
            }
        },
        "required": ["project_id", "page", "size", "status"]
    }
)
async def get_project_milestones(project_id: str, page: int, size: int, status: str) -> list[types.TextContent]:
    response: list[MilestoneInfo] = await project.get_project_milestones(project_id=project_id, page=page, size=size, status=status)
    return converter.convert_mcp_text_output(response)

@server.register_tool(
    description="""
    get project tags.
    it is used for getting tag(syn. label, ...) list of project.
    """,
    inputSchema={
        "type": "object",
        "properties": {
            "project_id": {
                "type": "string",
                "description":
                """
                target project id to get tag list.
                """
            },
            "page": {
                "type": "integer",
                "description":
                """
                page number(0 base), Default value : 0
                """
            },
            "size": {
                "type": "integer",
                "description":
                """
                page size, Default value : 100, max value: 100
                """
            }
        },
        "required": ["project_id", "page", "size"]
    }
)
async def get_project_tags(project_id: str, page: int, size: int) -> list[types.TextContent]:
    response: list[TagInfo] = await project.get_project_tags(project_id=project_id, page=page, size=size)
    return converter.convert_mcp_text_output(response)