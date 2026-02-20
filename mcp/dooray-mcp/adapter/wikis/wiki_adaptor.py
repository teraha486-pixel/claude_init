import httpx
from adapter.dooray import DoorayApiClient
from model.wiki.request.wiki import CreateWiki, WikiModifyBody
from model.wiki.response.wiki import WikiBrief, WikiPage
from model.dooray import ApiResponse

WIKI_URL = "https://api.dooray.com/wiki/v1/wikis"
WIKI_PAGE_URL = "https://api.dooray.com/wiki/v1/pages"

async def get_wiki_list(page: int, size: int) -> list[WikiBrief]:

    async with DoorayApiClient.default_client() as client:
        response: httpx.Response = await client.get(f"{WIKI_URL}", params={"page": page, "size": size})
        api_response = ApiResponse(**response.json())

        if api_response.result is None or not isinstance(api_response.result, list):
            raise ValueError("Invalid response format: expected a list of wikis.")
        
        wikis = [WikiBrief(**kwargs) for kwargs in api_response.result]
    return wikis

async def get_child_wiki_list(wiki_id: str, parentPageId: str | None) -> list[WikiPage]:

    async with DoorayApiClient.default_client() as client:
        response: httpx.Response = await client.get(f"{WIKI_URL}/{wiki_id}/pages", params={"parentPageId": parentPageId})
        api_response = ApiResponse(**response.json())

        if api_response.result is None or not isinstance(api_response.result, list):
            raise ValueError("Invalid response format: expected a list of wikis.")
        
        wikis = [WikiPage(**kwargs) for kwargs in api_response.result]
    return wikis

async def create_wiki(request: CreateWiki, wiki_id: str) -> httpx.Response:
    async with DoorayApiClient.default_client() as client:
        response = await client.post(f'{WIKI_URL}/{wiki_id}/pages',
                                   content=request.model_dump_json(by_alias=True))
    return response

async def get_wiki_page_content(wiki_id: str, page_id: str) -> httpx.Response:
    async with DoorayApiClient.default_client() as client:
        response = await client.get(f"{WIKI_URL}/{wiki_id}/pages/{page_id}")
    return response

async def get_wiki_page_by_id(page_id: str) -> httpx.Response:
    """
    페이지 ID만으로 위키 페이지의 상세 정보를 조회합니다.
    프로젝트 ID 없이 페이지 ID만 알면 조회할 수 있습니다.
    """
    async with DoorayApiClient.default_client() as client:
        response = await client.get(f"{WIKI_PAGE_URL}/{page_id}")
    return response

async def upload_file_to_wiki(wiki_id: str, page_id: str, file_path: str) -> str:
    async with DoorayApiClient.file_upload_client() as client:
        response: str = await client.redirect_post_with_file(f'{WIKI_URL}/{wiki_id}/pages/{page_id}/files', file_path=file_path, data={"type": "general"})
    return response

async def modify_wiki_page(wiki_id: str, page_id: str, content: str) -> httpx.Response:
    async with DoorayApiClient.default_client() as client:
        response = await client.put(f'{WIKI_URL}/{wiki_id}/pages/{page_id}/content', content=WikiModifyBody.from_content(content).model_dump_json(by_alias=True))
    return response

# 위키 페이지 댓글 관련 함수들
async def get_wiki_page_comments(wiki_id: str, page_id: str, page: int = 0, size: int = 20) -> httpx.Response:
    """위키 페이지의 댓글 목록을 조회합니다."""
    async with DoorayApiClient.default_client() as client:
        response = await client.get(
            f'{WIKI_URL}/{wiki_id}/pages/{page_id}/comments',
            params={"page": page, "size": size}
        )
    return response

async def create_wiki_page_comment(wiki_id: str, page_id: str, content: str, mime_type: str = "text/x-markdown") -> httpx.Response:
    """위키 페이지에 댓글을 생성합니다."""
    import json
    body = {
        "body": {
            "content": content,
            "mimeType": mime_type
        },
        "attachFileIds": []
    }
    async with DoorayApiClient.default_client() as client:
        response = await client.post(
            f'{WIKI_URL}/{wiki_id}/pages/{page_id}/comments',
            content=json.dumps(body)
        )
    return response

async def update_wiki_page_comment(wiki_id: str, page_id: str, log_id: str, content: str, mime_type: str = "text/x-markdown") -> httpx.Response:
    """위키 페이지의 댓글을 수정합니다."""
    import json
    body = {
        "body": {
            "content": content,
            "mimeType": mime_type
        }
    }
    async with DoorayApiClient.default_client() as client:
        response = await client.put(
            f'{WIKI_URL}/{wiki_id}/pages/{page_id}/comments/{log_id}',
            content=json.dumps(body)
        )
    return response

async def delete_wiki_page_comment(wiki_id: str, page_id: str, log_id: str) -> httpx.Response:
    """위키 페이지의 댓글을 삭제합니다."""
    async with DoorayApiClient.default_client() as client:
        response = await client.delete(
            f'{WIKI_URL}/{wiki_id}/pages/{page_id}/comments/{log_id}'
        )
    return response