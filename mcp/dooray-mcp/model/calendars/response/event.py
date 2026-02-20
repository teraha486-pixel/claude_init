from pydantic import BaseModel, Field, ConfigDict
from model.types.deref_model import DerefModel

class CalendarSimpleInfo(DerefModel):
    id: str
    name: str

class ConferenceInfo(DerefModel):
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True, extra='ignore')

    service_type: str | None = Field(alias='serviceType', default=None)

class ScheduleUserInfo(DerefModel):
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True, extra='ignore')

    user_type: str | None = Field(alias='userType', default=None)
    status: str | None = None
class EventResponse(DerefModel):
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True, extra='ignore')

    id: str
    calendar: CalendarSimpleInfo | None = None
    recurrence_id: str | None = Field(alias='recurrenceId', default=None)
    started_at: str | None = Field(alias='startedAt', default=None)
    ended_at: str | None = Field(alias='endedAt', default=None)
    location: str | None = None
    subject: str | None = None
    whole_day_flag: bool = Field(alias='wholeDayFlag')
    conferencing: ConferenceInfo | None = None
    me: ScheduleUserInfo | None = None
