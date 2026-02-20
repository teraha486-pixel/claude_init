from mcp.types import TextContent
from pydantic import BaseModel
from typing import TypeVar, List, Union, Generic

# BaseModel을 상속한 클래스만 허용하는 타입 변수
T = TypeVar('T', bound=BaseModel)

def convert_mcp_text_output_list(contents: List[T]) -> List[TextContent]:
    return [TextContent(type="text", text=c.model_dump_json()) for c in contents]

def convert_mcp_text_output(content: Union[T, List[T]]) -> List[TextContent]:
    if isinstance(content, list):
        return convert_mcp_text_output_list(content)
    else:
        return convert_mcp_text_output_list([content])
