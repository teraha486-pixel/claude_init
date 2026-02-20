from model.types.deref_model import DerefModel

class CalendarAttributes(DerefModel):
    role: str
    default: bool

class CalendarInfo(DerefModel):
    id: str
    name: str
    type: str
    me: CalendarAttributes