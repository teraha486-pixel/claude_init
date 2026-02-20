import httpx
import server
import mcp.types as types
from datetime import datetime

from adapter.calendars import calendar as calendar_adapter
from model.calendars.request.event import Event
from model.types import empty_input_schema

from model.calendars.response.event import EventResponse
from model.dooray import ApiResponse
from model.calendars.request import calendar
from utils import converter

@server.register_tool(
    description="""
    get list of my calendars.
    if the user provided no mention about calendar to be searched, it would be searched private default calendar.
    """,
    inputSchema=empty_input_schema
)
async def get_my_calendars() -> list[types.TextContent]:
    # list of calendars
    response: list[calendar.CalendarInfo]= await calendar_adapter.get_my_calendars()
    return converter.convert_mcp_text_output(response)

@server.register_tool(
    description='get detail information about a specific calendar',
    inputSchema={
        "type": "object",
        "properties": {
            "calendar_id": {
                "type": "string",
                "description": "ID of calendar to fetch details for"
            }
        },
        "required": ["calendar_id"]
    }
)
async def get_detail_of_calendar(calendar_id: str) -> list[types.TextContent]:
    response: httpx.Response = await calendar_adapter.get_detail_of_calendar(calendar_id)
    return [types.TextContent(type="text", text=str(response.text))]

@server.register_tool(
    description="""
            create a event to specific calendar. before create a event, you have to get a detail information of calendar that you will create a event to because of default alarm method.
            if you want to create a event to multiple calendars, you have to call this tool multiple times.
            """,
    inputSchema={
        "type": "object",
        "properties": {
            "calendar_id": {
                "type": "string",
                "description": "ID of calendar to fetch details for"
            },
            "event": Event.model_json_schema()
        },
        "required": ["calendar_id", "event"]
    }
)
async def create_event_to_calendar(calendar_id: str, event: dict) -> list[types.TextContent]:
    response: httpx.Response = await calendar_adapter.create_calendar_event(calendar_id, Event(**event))
    return [types.TextContent(type="text", text=response.text)]

@server.register_tool(
    description="""
    get all events of my calendars.
    if the user provided no mention about calendar to be searched, it would be searched personal private default calendar. try get_my_calendars() tool to get user's calendars.
    This tool can search schedules up to 1 month apart. if you want to search events over a period of more than one month, you must call this tool several times.
    """,
    inputSchema={
        "type": "object",
        "properties": {
            "time_min": {
                "type": "string",
                "description": "start time to search event (e.g., '%Y-%m-%dT%H:%M:%S%z', default timezone is Asia/Seoul(+09:00).)"
            },
            "time_max": {
                "type": "string",
                "description": "end time to search event (e.g., '%Y-%m-%dT%H:%M:%S%z', default timezone is Asia/Seoul(+09:00).)"
            },
            "calendars": {
                "type": "array",
                "description": "calendar id string array to search events from. if the user provided no mention about calendar to be searched, it would be searched personal private default calendar.",
                "items": { "type": "string" }
            }
        },
        "required": ["time_min", "time_max", "calendars"]
    }
)
async def get_all_events_of_calendars(time_min: str, time_max: str, calendars: list[str]) -> list[types.TextContent]:
    response: list[EventResponse] = await calendar_adapter.get_all_events(
        datetime.fromisoformat(time_min), datetime.fromisoformat(time_max), calendars
    )
    return converter.convert_mcp_text_output(response)

@server.register_tool(
    description='get detail information about a specific event on calendar',
    inputSchema={
        "type": "object",
        "properties": {
            "calendar_id": {
                "type": "string",
                "description": "calendar id string to search event from"
            },
            "event_id": {
                "type": "string",
                "description": "event id string to get detail infos"
            }
        },
        "required": ["calendar_id", "event_id"]
    }
)
async def get_detail_of_event_on_calendar(calendar_id: str, event_id: str) -> list[types.TextContent]:
    response: httpx.Response = await calendar_adapter.get_detail_of_event(calendar_id, event_id)
    return [types.TextContent(type="text", text=response.text)]

@server.register_tool(
    description='delete a specific event from calendar. Must be reviewed detail of event that will be deleted.',
    inputSchema={
        "type": "object",
        "properties": {
            "calendar_id": {
                "type": "string",
                "description": "calendar id string to search event from"
            },
            "event_id": {
                "type": "string",
                "description": "event id string that will be deleted"
            },
            "event_type": {
                "type": "string",
                "description": """
                event type to be deleted. only allowed values are 'this', 'whole', 'wholeFromThis'.
                'this': delete only this event.
                'whole': delete all events that is recurrencing
                'wholeFromThis': delete all events that is recurrencing after this event.
                """
            }
        },
        "required": ["calendar_id", "event_id"]
    }
)
async def delete_event_from_calendar(calendar_id: str, event_id: str, event_type: str) -> list[types.TextContent]:
    response: httpx.Response = await calendar_adapter.delete_event_from_calendar(calendar_id, event_id, event_type)
    return [types.TextContent(type="text", text=response.text)]

