import httpx
import server
import mcp.types as types

from adapter.reservations import reservation as reservation_adapter


@server.register_tool(
    description='자원 유형(카테고리) 목록을 조회합니다. 회의실(meetingRoom), 사무기기(oa), 휴대폰(mobile), 차량(vehicle) 등의 유형을 확인할 수 있습니다.',
    inputSchema={
        "type": "object",
        "properties": {},
    }
)
async def get_resource_categories() -> list[types.TextContent]:
    response: httpx.Response = await reservation_adapter.get_resource_categories()
    return [types.TextContent(type="text", text=response.text)]


@server.register_tool(
    description='예약 가능한 자원 목록을 조회합니다. resource_category_id로 특정 유형의 자원만 필터링할 수 있습니다. 자원 예약 전 이 도구로 예약 가능한 자원 ID를 먼저 확인하세요.',
    inputSchema={
        "type": "object",
        "properties": {
            "resource_category_id": {
                "type": "string",
                "description": "자원 유형 ID로 필터링 (선택). get_resource_categories로 확인 가능."
            }
        },
    }
)
async def get_reservable_resources(resource_category_id: str = None) -> list[types.TextContent]:
    response: httpx.Response = await reservation_adapter.get_reservable_resources(resource_category_id)
    return [types.TextContent(type="text", text=response.text)]


@server.register_tool(
    description='자원 상세 정보를 조회합니다. 운영시간, 예약단위, 수용인원 등 상세 정보를 확인할 수 있습니다.',
    inputSchema={
        "type": "object",
        "properties": {
            "resource_id": {
                "type": "string",
                "description": "조회할 자원 ID"
            }
        },
        "required": ["resource_id"]
    }
)
async def get_resource_detail(resource_id: str) -> list[types.TextContent]:
    response: httpx.Response = await reservation_adapter.get_resource_detail(resource_id)
    return [types.TextContent(type="text", text=response.text)]


@server.register_tool(
    description='특정 기간의 자원 예약 목록을 조회합니다. 회의실 등 자원의 예약 현황을 확인할 수 있습니다.',
    inputSchema={
        "type": "object",
        "properties": {
            "time_min": {
                "type": "string",
                "description": "조회 시작 시간 (ISO8601 형식, 예: 2026-03-12T00:00:00+09:00)"
            },
            "time_max": {
                "type": "string",
                "description": "조회 종료 시간 (ISO8601 형식, 예: 2026-03-13T00:00:00+09:00)"
            },
            "resource_ids": {
                "type": "array",
                "items": {"type": "string"},
                "description": "조회할 자원 ID 목록 (선택, 미지정 시 전체 자원)"
            }
        },
        "required": ["time_min", "time_max"]
    }
)
async def get_resource_reservations(time_min: str, time_max: str, resource_ids: list[str] = None) -> list[types.TextContent]:
    response: httpx.Response = await reservation_adapter.get_resource_reservations(time_min, time_max, resource_ids)
    return [types.TextContent(type="text", text=response.text)]


@server.register_tool(
    description="""자원을 예약합니다. 예약 전 get_reservable_resources로 자원 ID를 확인하고, get_resource_reservations로 해당 시간대 예약 가능 여부를 확인하세요.
    반복 예약 시 recurrence_rule을 설정합니다. frequency: daily/weekly/monthly/yearly, byday: SU,MO,TU,WE,TH,FR,SA""",
    inputSchema={
        "type": "object",
        "properties": {
            "resource_id": {
                "type": "string",
                "description": "예약할 자원 ID"
            },
            "subject": {
                "type": "string",
                "description": "예약명/내용"
            },
            "started_at": {
                "type": "string",
                "description": "예약 시작 시간 (ISO8601 형식, 예: 2026-03-12T14:00:00+09:00)"
            },
            "ended_at": {
                "type": "string",
                "description": "예약 종료 시간 (ISO8601 형식, 예: 2026-03-12T15:00:00+09:00)"
            },
            "whole_day_flag": {
                "type": "boolean",
                "description": "종일 예약 여부 (기본값: false)",
                "default": False
            },
            "recurrence_rule": {
                "type": "object",
                "description": "반복 예약 규칙 (선택)",
                "properties": {
                    "frequency": {"type": "string", "description": "반복 주기: daily, weekly, monthly, yearly"},
                    "interval": {"type": "integer", "description": "반복 간격 (예: 2주마다 = interval:2)"},
                    "until": {"type": "string", "description": "반복 종료 시간 (ISO8601)"},
                    "byday": {"type": "string", "description": "요일 목록: SU,MO,TU,WE,TH,FR,SA"},
                    "bymonthday": {"type": "string", "description": "일 목록: 1~31"},
                    "bymonth": {"type": "string", "description": "월 목록: 1~12"},
                    "timezoneName": {"type": "string", "description": "타임존 (기본: Asia/Seoul)"}
                }
            }
        },
        "required": ["resource_id", "subject", "started_at", "ended_at"]
    }
)
async def create_resource_reservation(resource_id: str, subject: str, started_at: str, ended_at: str, whole_day_flag: bool = False, recurrence_rule: dict = None) -> list[types.TextContent]:
    body = {
        "resourceId": resource_id,
        "subject": subject,
        "startedAt": started_at,
        "endedAt": ended_at,
        "wholeDayFlag": whole_day_flag,
        "class": "public"
    }
    if recurrence_rule:
        body["recurrenceRule"] = recurrence_rule
    response: httpx.Response = await reservation_adapter.create_resource_reservation(body)
    return [types.TextContent(type="text", text=response.text)]


@server.register_tool(
    description='자원 예약 상세 정보를 조회합니다.',
    inputSchema={
        "type": "object",
        "properties": {
            "resource_reservation_id": {
                "type": "string",
                "description": "예약 ID. 반복 예약 중 특정 건 조회 시 '{id}-{yyyyMMddTHHmmssZ}' 형식 사용"
            }
        },
        "required": ["resource_reservation_id"]
    }
)
async def get_resource_reservation_detail(resource_reservation_id: str) -> list[types.TextContent]:
    response: httpx.Response = await reservation_adapter.get_resource_reservation_detail(resource_reservation_id)
    return [types.TextContent(type="text", text=response.text)]


@server.register_tool(
    description='자원 예약을 수정합니다. 반복 예약의 경우 update_type으로 수정 범위를 지정합니다.',
    inputSchema={
        "type": "object",
        "properties": {
            "resource_reservation_id": {
                "type": "string",
                "description": "수정할 예약 ID"
            },
            "subject": {
                "type": "string",
                "description": "예약명/내용"
            },
            "started_at": {
                "type": "string",
                "description": "예약 시작 시간 (ISO8601)"
            },
            "ended_at": {
                "type": "string",
                "description": "예약 종료 시간 (ISO8601)"
            },
            "whole_day_flag": {
                "type": "boolean",
                "description": "종일 예약 여부",
                "default": False
            },
            "update_type": {
                "type": "string",
                "description": "수정 범위: whole(전체 반복), this(이 예약만), wholeFromThis(이후 모두). 반복 예약이 아니면 생략.",
                "enum": ["whole", "this", "wholeFromThis"]
            }
        },
        "required": ["resource_reservation_id", "subject", "started_at", "ended_at"]
    }
)
async def update_resource_reservation(resource_reservation_id: str, subject: str, started_at: str, ended_at: str, whole_day_flag: bool = False, update_type: str = None) -> list[types.TextContent]:
    body = {
        "subject": subject,
        "startedAt": started_at,
        "endedAt": ended_at,
        "wholeDayFlag": whole_day_flag,
        "class": "public"
    }
    if update_type:
        body["updateType"] = update_type
    response: httpx.Response = await reservation_adapter.update_resource_reservation(resource_reservation_id, body)
    return [types.TextContent(type="text", text=response.text)]


@server.register_tool(
    description='자원 예약을 삭제합니다. 반복 예약의 경우 delete_type으로 삭제 범위를 지정합니다.',
    inputSchema={
        "type": "object",
        "properties": {
            "resource_reservation_id": {
                "type": "string",
                "description": "삭제할 예약 ID"
            },
            "delete_type": {
                "type": "string",
                "description": "삭제 범위: whole(전체 반복 삭제), this(이 예약만), wholeFromThis(이후 모두). 반복 예약이 아니면 빈 문자열.",
                "default": ""
            }
        },
        "required": ["resource_reservation_id"]
    }
)
async def delete_resource_reservation(resource_reservation_id: str, delete_type: str = '') -> list[types.TextContent]:
    response: httpx.Response = await reservation_adapter.delete_resource_reservation(resource_reservation_id, delete_type)
    return [types.TextContent(type="text", text=response.text)]
