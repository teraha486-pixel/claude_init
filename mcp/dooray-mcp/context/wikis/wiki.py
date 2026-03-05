import httpx
import server
import mcp.types as types
from adapter.wikis import wiki_adaptor
from model.wiki.request.wiki import CreateWiki
from model.wiki.response.wiki import WikiBrief, WikiPage
from utils import converter
import jsonref

@server.register_tool(
    description='get wiki domain list which is able to access. pagenation is supported.',
    inputSchema={
    "type": "object",
    "properties": {
        "page": {
            "type": "integer",
            "description": 
            """
            page number(0 base), Default value : 0
            """
        },
        "size": {
            "type": "integer",
            "description": 
            """
            page size, Default value : 100, max value: 100
            """
        },
    },
    "required": ["page", "size"]
    }
)
async def get_wiki_list(page: int, size: int):
        response: list[WikiBrief] = await wiki_adaptor.get_wiki_list(page, size)
        return converter.convert_mcp_text_output(response)

@server.register_tool(
    description="get child wiki list which is a selected wiki Page's child. if you want to get deeper child page, please use this function recursively.",
    inputSchema={
    "type": "object",
    "properties": {
        "parentPageId": {
            "type": "string",
            "description": 
            """
            Parent wiki page ID to search on it(if null, retrieves top-level pages).
            """
        },
        "wiki_id": {
            "type": "string",
            "description": 
            """
            wiki domain id to get child wiki page
            """
        }
    },
    "required": ["wiki_id"]
    }
)
async def get_child_wiki_list(wiki_id: str, parentPageId: str | None = None):
        response: list[WikiPage] = await wiki_adaptor.get_child_wiki_list(wiki_id, parentPageId)
        return converter.convert_mcp_text_output(response)

@server.register_tool(
    description="""
    wiki page creating tool.
    this tool would create a wiki page on a specific wiki domain. 
    If you want to create wiki page at the child page, please use get child wiki list first.
    """,
    inputSchema={
    "type": "object",
    "properties": {
        "request": CreateWiki.model_json_schema(),
        "wiki_id": {
            "type": "string",
            "description": 
            """
            wiki domain id to create a wiki page
            """
        }
    },
    "required": ["request", "wiki_id"]
    }
)
async def create_wiki(request: dict, wiki_id:str):
    response: httpx.Response = await wiki_adaptor.create_wiki(CreateWiki(**request), wiki_id)
    return [types.TextContent(type="text", text=response.text)]

@server.register_tool(
    description="get wiki page content.",
    inputSchema={
        "type": "object",
        "properties": {
            "wiki_id": {
                "type": "string",
                "description": 
                """
                wiki domain id to get a wiki page content
                """
            },
            "page_id": {
                "type": "string",
                "description": 
                """
                wiki page id to get a wiki page content
                """
            }
        },
        "required": ["wiki_id", "page_id"]
    }
)
async def get_wiki_page_content(wiki_id: str, page_id: str):
    response: httpx.Response = await wiki_adaptor.get_wiki_page_content(wiki_id, page_id)
    return [types.TextContent(type="text", text=response.text)]

@server.register_tool(
    description="""
    페이지 ID만으로 두레이 위키 페이지의 상세 정보를 조회합니다.
    wiki_id 없이 페이지 ID만 알면 조회할 수 있습니다.

    두레이 위키 URL (예: https://nhnent.dooray.com/wiki/{wiki_id}/{page_id})에서
    마지막 숫자({page_id})가 page_id입니다.
    """,
    inputSchema={
        "type": "object",
        "properties": {
            "page_id": {
                "type": "string",
                "description": "위키 페이지 ID (두레이 URL에서 확인 가능)"
            }
        },
        "required": ["page_id"]
    }
)
async def get_wiki_page_by_id(page_id: str):
    response: httpx.Response = await wiki_adaptor.get_wiki_page_by_id(page_id)
    return [types.TextContent(type="text", text=response.text)]

SEARCH_RANGE=50

@server.register_tool(
    description="get a personal(private) wiki.",
    inputSchema={
    "type": "object",
    "properties": {},
    "required": []
    }
)
async def get_personal_wiki():
    i = 0
    while True:
        response: list[WikiBrief] = await wiki_adaptor.get_wiki_list(i, SEARCH_RANGE)
        priv_wiki = [wiki for wiki in response if wiki.type == "private"]
        i = i+1

        if len(priv_wiki) <= 0:
            if len(response) < SEARCH_RANGE:
                raise Exception("No personal wiki found")
        else:
            return [types.TextContent(type='text', text=priv_wiki[0].model_dump_json())]
        
@server.register_tool(
    description="""
    upload a file to wiki page.
    if you want to post a image to wiki page, first, wiki page must be exist that image would be uploaded.
    and then, that image would be uploaded to wiki page was created already.
    and then, modify the wiki page with given pageFileId as result of this tool.
    """,
    inputSchema={
        "type": "object",
        "properties": {
            "wiki_id": {
                "type": "string",
                "description": 
                """
                wiki domain id to upload a file
                """
            },
            "page_id": {
                "type": "string",
                "description": 
                """
                wiki page ID to upload a file
                """
            },
            "file_path": {
                "type": "string",
                "description": 
                """
                local file full path to upload
                """
            }
        },
        "required": ["wiki_id", "page_id", "file_path"]
    }
)
async def upload_file_to_wiki(wiki_id: str, page_id: str, file_path: str):
    response: str = await wiki_adaptor.upload_file_to_wiki(wiki_id, page_id, file_path)
    return [types.TextContent(type="text", text=response)]

@server.register_tool(
    description="""
    modify wiki page.
    if you want to post a image to wiki page, you must upload that image first using upload_file_to_wiki tool.
    and then, make a path to that image with given pageFileId as result of upload_file_to_wiki tool.
    wiki image url format is like this:
    ![](/page-files/{pageFileId})

    and then, modify the wiki page content with that markdown image format.
    """,
    inputSchema={
        "type": "object",
        "properties": {
            "wiki_id": {
                "type": "string",
                "description": 
                """
                wiki domain id to upload a file
                """
            },
            "page_id": {
                "type": "string",
                "description": 
                """
                wiki page id to modify
                """
            },
            "content": {
                "type": "string",
                "description": 
                """
                wiki page content to modify.
                text/x-markdown format content.

                if you want to post a image to wiki page, you must upload that image first using upload_file_to_wiki tool.
                and then, make a path to that image with given pageFileId as result of upload_file_to_wiki tool.
                wiki image url format is like this:
                ![](/page-files/{pageFileId})

                and then, modify the wiki page content with that markdown image format.
                """
            }
        },
        "required": ["wiki_id", "page_id", "content"]
    }
)
async def modify_wiki_page(wiki_id: str, page_id: str, content: str):
    response: httpx.Response = await wiki_adaptor.modify_wiki_page(wiki_id, page_id, content)
    return [types.TextContent(type="text", text=response.text)]

# 위키 페이지 댓글 관련 도구들
@server.register_tool(
    description="위키 페이지의 댓글 목록을 조회합니다.",
    inputSchema={
        "type": "object",
        "properties": {
            "wiki_id": {
                "type": "string",
                "description": "위키 도메인 ID"
            },
            "page_id": {
                "type": "string",
                "description": "위키 페이지 ID"
            },
            "page": {
                "type": "integer",
                "description": "페이지 번호 (0부터 시작, 기본값: 0)"
            },
            "size": {
                "type": "integer",
                "description": "페이지 크기 (기본값: 20)"
            }
        },
        "required": ["wiki_id", "page_id"]
    }
)
async def get_wiki_page_comments(wiki_id: str, page_id: str, page: int = 0, size: int = 20):
    response: httpx.Response = await wiki_adaptor.get_wiki_page_comments(wiki_id, page_id, page, size)
    return [types.TextContent(type="text", text=response.text)]

@server.register_tool(
    description="위키 페이지에 댓글을 생성합니다.",
    inputSchema={
        "type": "object",
        "properties": {
            "wiki_id": {
                "type": "string",
                "description": "위키 도메인 ID"
            },
            "page_id": {
                "type": "string",
                "description": "위키 페이지 ID"
            },
            "content": {
                "type": "string",
                "description": "댓글 내용 (Markdown 형식 지원)"
            },
            "mime_type": {
                "type": "string",
                "description": "MIME 타입 (기본값: text/x-markdown)"
            }
        },
        "required": ["wiki_id", "page_id", "content"]
    }
)
async def create_wiki_page_comment(wiki_id: str, page_id: str, content: str, mime_type: str = "text/x-markdown"):
    response: httpx.Response = await wiki_adaptor.create_wiki_page_comment(wiki_id, page_id, content, mime_type)
    return [types.TextContent(type="text", text=response.text)]

@server.register_tool(
    description="위키 페이지의 댓글을 수정합니다.",
    inputSchema={
        "type": "object",
        "properties": {
            "wiki_id": {
                "type": "string",
                "description": "위키 도메인 ID"
            },
            "page_id": {
                "type": "string",
                "description": "위키 페이지 ID"
            },
            "log_id": {
                "type": "string",
                "description": "댓글 ID (get_wiki_page_comments로 조회 가능)"
            },
            "content": {
                "type": "string",
                "description": "수정할 댓글 내용 (Markdown 형식 지원)"
            },
            "mime_type": {
                "type": "string",
                "description": "MIME 타입 (기본값: text/x-markdown)"
            }
        },
        "required": ["wiki_id", "page_id", "log_id", "content"]
    }
)
async def update_wiki_page_comment(wiki_id: str, page_id: str, log_id: str, content: str, mime_type: str = "text/x-markdown"):
    response: httpx.Response = await wiki_adaptor.update_wiki_page_comment(wiki_id, page_id, log_id, content, mime_type)
    return [types.TextContent(type="text", text=response.text)]

@server.register_tool(
    description="위키 페이지의 댓글을 삭제합니다.",
    inputSchema={
        "type": "object",
        "properties": {
            "wiki_id": {
                "type": "string",
                "description": "위키 도메인 ID"
            },
            "page_id": {
                "type": "string",
                "description": "위키 페이지 ID"
            },
            "log_id": {
                "type": "string",
                "description": "삭제할 댓글 ID (get_wiki_page_comments로 조회 가능)"
            }
        },
        "required": ["wiki_id", "page_id", "log_id"]
    }
)
async def delete_wiki_page_comment(wiki_id: str, page_id: str, log_id: str):
    response: httpx.Response = await wiki_adaptor.delete_wiki_page_comment(wiki_id, page_id, log_id)
    return [types.TextContent(type="text", text=response.text)]