from pydantic import Field
from model.types.deref_model import DerefModel

class Pageable(DerefModel):
    page: int = Field(default=0, description="0-based Page number to retrieve.")
    size: int = Field(default=50, description="Number of items per page.")
