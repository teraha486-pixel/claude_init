from datetime import datetime
import mcp.types as types

import server

from model.types import empty_input_schema
from adapter.common import common as common_adaptor 
from model.dooray import ApiResponse

@server.register_tool(
    description='get current date and time',
    inputSchema=empty_input_schema
)
async def get_date_time_now():
    return [types.TextContent(type="text", text=datetime.now().astimezone().isoformat(timespec='seconds'))]

@server.register_tool(
    description='get members information. usually used for getting organizationMemberId. organizationMemberId == memberId == id',
    inputSchema={
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "member name to find with"
            },
            "page": {
                "type": "integer",
                "description": "page number to find with. 0-indexed. default is 0"
            },
            "size": {
                "type": "integer",
                "description": "size of page to find with. default is 20, maximum size is 100"
            }
        },
        "required": ["name", "page", "size"]
    }
)
async def get_members_information_by_name(name: str, page: int, size: int) -> list[types.TextContent]:
    response = await common_adaptor.get_members_information_by_name(name, page, size)
    return [types.TextContent(type="text", text=response.text)]

@server.register_tool(
    description="""
    get my member information. 
    it would be used for some tools that need my member identifier such as registration as task assignee.
    """,
    inputSchema=empty_input_schema
)
async def get_my_member_identifier() -> list[types.TextContent]:
    response = await common_adaptor.get_my_member_identities()
    return [types.TextContent(type="text", text=response.text)]
