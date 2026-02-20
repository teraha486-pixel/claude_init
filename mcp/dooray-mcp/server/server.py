import mcp.types as types
from collections.abc import Callable
from utils.logger import logger

tools: dict[str, Callable] = {}
tool_descriptions: dict[str, types.Tool] = {}

class McpToolException(Exception):
    def __init__(self, message: str):
        logger.error(f'{message}')
        super().__init__(message)

class UndefinedToolException(McpToolException):
    def __init__(self, tool_name: str):
        super().__init__(f'Undefined tool exception, check tool name: [called_tool_name={tool_name}]')

class DuplicatedToolNameException(McpToolException):
    def __init__(self, tool_name: str):
        super().__init__(f'Duplicated tool or function name, check tool name: [called_tool_name={tool_name}]')

def register_tool(**kwargs):
    def decorator(func):
        tools[func.__name__] = func
        if func.__name__ not in tool_descriptions:
            tool_descriptions[func.__name__] = types.Tool(name=func.__name__,**kwargs)
        else:
            raise DuplicatedToolNameException(func.__name__)
        return func

    return decorator

from mcp.server import Server

server = Server(name='dooray-mcp')

@server.call_tool()
async def call_tools_delegator(name: str, arguments: dict) -> list[types.TextContent | types.EmbeddedResource | types.ImageContent]:
    logger.info(f'Calling tool: [name={name}, arguments={arguments}]')
    if name not in tools:
        raise UndefinedToolException(name)
    else:
        output = await tools[name](**arguments)
        logger.info(f'Tool output: [name={name}, output={output}]')
        return output

@server.list_tools()
async def list_tools():
    return [v for k, v in tool_descriptions.items()]