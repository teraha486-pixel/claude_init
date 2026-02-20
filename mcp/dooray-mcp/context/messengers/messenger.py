import httpx
import mcp.types as types

from adapter.messengers import messenger as messenger_adapter
import server
from model.types import empty_input_schema
from model.messenger.response.channel import ChannelInfo
from utils import converter

@server.register_tool(
    description='send a message to organization member directly',
    inputSchema={
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "a message to send to opponent"
            },
            "organization_member_id": {
                "type": "string",
                "description": "destination member id in organization to send a message"
            }
        },
        "required": ["text", "organization_member_id"]
    }
)
async def send_message_to_member_directly(text: str, organization_member_id: str) -> list[types.TextContent]:
    response: httpx.Response = await messenger_adapter.send_message_directly(text, organization_member_id)
    return [types.TextContent(type="text", text=response.text)]

@server.register_tool(
    description='get channel list from dooray messenger that i belongs to',
    inputSchema=empty_input_schema
)
async def get_channels_belongs_to() -> list[types.TextContent]:
    response: list[ChannelInfo] = await messenger_adapter.get_channels_belonged_to()
    return converter.convert_mcp_text_output(response)

@server.register_tool(
    description='send a message to channel',
    inputSchema={
        "type": "object",
        "properties": {
            "channel_id": {
                "type": "string",
                "description": "destination channel id to send a message"
            },
            "text": {
                "type": "string",
                "description": "a message to send to channel"
            }
        },
        "required": ["channel_id", "text"]
    }
)
async def send_message_to_channel(channel_id: str, text: str) -> list[types.TextContent]:
    response: httpx.Response = await messenger_adapter.send_message_to_channel(channel_id, text)
    return [types.TextContent(type="text", text=response.text)]

@server.register_tool(
    description='modify message that i sent to channel before',
    inputSchema={
        "type": "object",
        "properties": {
            "channel_id": {
                "type": "string",
                "description": "destination channel id to modify a message"
            },
            "log_id": {
                "type": "string",
                "description": "a message id to modify"
            },
            "text": {
                "type": "string",
                "description": "text to replace message"
            }
        },
        "required": ["channel_id", "log_id", "text"]
    }
)
async def modify_message_sent_to_channel(
        channel_id: str,
        log_id: str,
        text: str
) -> list[types.TextContent]:
    response: httpx.Response = await messenger_adapter.modify_message_sent_to_channel(channel_id, log_id, text)
    return [types.TextContent(type="text", text=response.text)]

@server.register_tool(
    description='delete message that i sent to channel before',
    inputSchema={
        "type": "object",
        "properties": {
            "channel_id": {
                "type": "string",
                "description": "destination channel id to delete a message"
            },
            "log_id": {
                "type": "string",
                "description": "a message id to delete"
            }
        },
        "required": ["channel_id", "log_id"]
    }
)
async def delete_message_sent_to_channel(channel_id: str,log_id: str) -> list[types.TextContent]:
    response: httpx.Response = await messenger_adapter.delete_message_sent_to_channel(channel_id, log_id)
    return [types.TextContent(type="text", text=response.text)]
