from pydantic import ConfigDict, Field
from model.dooray import OrganizationMember
from enum import Enum
from datetime import datetime
from typing import Any
from model.types.deref_model import DerefModel

class EventBody(DerefModel):
    mimeType: str = Field(description='"text/html" or "text/x-markdown"')
    content: str

class EventUser(DerefModel):
    type: str = Field(description='"member" or "department"')
    member: OrganizationMember

class ScheduleUsers(DerefModel):
    to: list[EventUser] = Field(description='except me when alone in event')
    cc: list[EventUser]

class EventFrequency(str, Enum):
    daily='daily'
    weekly='weekly'
    monthly='monthly'
    yearly='yearly'

class Day(str, Enum):
    sunday='SU'
    monday='MO'
    tuesday='TU'
    wednesday='WE'
    thursday='TH'
    friday='FR'
    saturday='ST'

class AlarmMethod(str, Enum):
    mail='mail'
    app='app'

class Alarm(DerefModel):
    action: AlarmMethod
    trigger: str = Field(description='RFC2445 format, duration, trigger. (ex. "TRIGGER:-PT10M"). if user mentioned anything about this, it will be applied default alarm settings of calendar.')

class AccessModifier(str, Enum):
    public='public'
    private='private'

class PersonalSettings(DerefModel):
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    alarms: list[Alarm] = Field(
        description='If there is no mention of this, default value is [(app, TRIGGER:-PT10M), (mail, TRIGGER:-PT10M)]', 
        default=[Alarm(action=AlarmMethod.app, trigger='TRIGGER:-PT10M'), Alarm(action=AlarmMethod.mail, trigger='TRIGGER:-PT10M')]
    )
    busy: bool = Field(description='true: i will be busy, false: i will be leisurely')
    class_: AccessModifier = Field(alias='class', description='default value is public, public: can be accessed everyone, private: can be only accessed by me')

class RecurrenceRule(DerefModel):
    model_config = ConfigDict(use_enum_values=True)

    frequency: EventFrequency | str = Field(description='required enum value', default="")
    interval: int | None = None
    until: datetime | str = Field(description='recurrent end day time, "" when rule has no end time', default="")
    byday: Day | str = Field(description='enum value or ""', default="")
    bymonth: int | str = Field(description='1 to 12 or ""', default="")
    bymonthday: int | str = Field(description='1 to 31 or ""', default="")
    timezoneName: str = Field(..., description='string of timezone (ex. "Asia/Seoul")')

class Event(DerefModel):
    model_config = ConfigDict(use_enum_values=True)

    users: ScheduleUsers = Field(description='users of event')
    subject: str = Field(description='subject of event')
    body: EventBody = Field(description='body of event, html or markdown format(text/x-markdown)')
    startedAt: datetime = Field(description='select appropriate time zone. (ex. when korean question, +09:00)')
    endedAt: datetime = Field(description='select appropriate time zone. (ex. when korean question, +09:00)')
    wholeDayFlag: bool = Field(description='true: whole day event, false: not whole day event')
    location: str = Field(description='location of event')
    recurrenceRule: RecurrenceRule | None = Field(description='recurrent rule of event. if user give no mention about recurrence rule, this field would be None', default=None) 
    personalSettings: PersonalSettings
