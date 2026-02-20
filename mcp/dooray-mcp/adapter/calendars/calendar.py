import httpx
from adapter.dooray import DoorayApiTokenContainer
from model.calendars.request import event, category, post_type, calendar
from datetime import datetime
from adapter.dooray import DoorayApiClient
from model.dooray import ApiResponse
from model.calendars.response.event import EventResponse

CALENDAR_PATH = 'https://api.dooray.com/calendar/v1'

async def get_my_calendars() -> list[calendar.CalendarInfo]:
    async with DoorayApiClient.default_client() as client:
        response = await client.get(f'{CALENDAR_PATH}/calendars')
    api_response = ApiResponse(**response.json())

    if api_response.result is None or not isinstance(api_response.result, list):
        raise ValueError("Invalid response format: expected a list of calendars.")

    calendars = [calendar.CalendarInfo(**kwargs) for kwargs in api_response.result]
    return calendars

async def get_detail_of_calendar(calendar_id: str) -> httpx.Response:
    async with DoorayApiClient.default_client() as client:
        response = await client.get(f'{CALENDAR_PATH}/calendars/{calendar_id}')
    return response

async def create_calendar_event(calendar_id: str, evt: event.Event) -> httpx.Response:
    async with DoorayApiClient.default_client() as client:
        response = await client.post(f"{CALENDAR_PATH}/calendars/{calendar_id}/events", content=evt.model_dump_json(by_alias=True))
    return response

async def get_all_events(time_min: datetime, time_max: datetime, calenders: list[str], post_type_: post_type.PostType | None=None, category_: category.Category | None=None) -> list[EventResponse]:
    async with DoorayApiClient.default_client() as client:
        response = await client.get(f"{CALENDAR_PATH}/calendars/*/events", params={
            'timeMin': time_min.isoformat(),
            'timeMax': time_max.isoformat(),
            'calendars': ','.join([str(i) for i in calenders]),
            # 'postType': post_type_,
            # 'category': category_
        })
        api_response = ApiResponse(**response.json())

    if api_response.result is None or not isinstance(api_response.result, list):
        raise ValueError("Invalid response format: expected a list of events.")
    
    events = [EventResponse(**kwargs) for kwargs in api_response.result]
    return events 

async def get_detail_of_event(calendar_id: str, event_id: str) -> httpx.Response:
    async with DoorayApiClient.default_client() as client:
        response = await client.get(f"{CALENDAR_PATH}/calendars/{calendar_id}/events/{event_id}")
    return response

# 이벤트 삭제 타입은 this. wholeFromThis: 해당 이벤트 이후 반복 이벤트 삭제, whole: 전체 반복 이벤트 삭제.
async def delete_event_from_calendar(calendar_id: str, event_id: str, event_type: str) -> httpx.Response:
    content = {
        'deleteType': event_type
    }
    async with DoorayApiClient.default_client() as client:
        response = await client.post(f"{CALENDAR_PATH}/calendars/{calendar_id}/events/{event_id}/delete", json=content)
    return response
