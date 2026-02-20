import httpx
from adapter.dooray import DoorayApiClient
from adapter.projects import project as project_adapter
from model.projects.request.task import CreateTask, ModifyTask, TaskQueryParam
from model.projects.response.project import ProjectInfo
from model.projects.response.task import TaskInfo, TaskDetail, TaskFullDetail
from model.dooray import ApiResponse
from utils.logger import logger

from .project import PROJECT_URL

# post_id만으로 조회하는 API endpoint
POST_URL = "https://api.dooray.com/project/v1/posts"

# 이거는 담당자, 참조자 등의 업무만 조회할 수 있도록 변경.
# 다른 쿼리 파라미터는 따로 함수를 분리할 것.
async def get_task_list_by_assignee_cc(project_id: list[str], asignee: str | None, cc: str | None) -> list[TaskInfo]:
    result: list[TaskInfo] = []

    task_query = TaskQueryParam(to_member_ids=asignee, cc_member_ids=cc)

    for pid in project_id:
        async with DoorayApiClient.default_client() as client:
            response:httpx.Response = await client.get(f'{PROJECT_URL}/{pid}/posts', params=task_query.model_dump(by_alias=True, exclude_none=True))
            api_response = ApiResponse(**response.json())

            if api_response.result is None or not isinstance(api_response.result, list):
                raise ValueError("Invalid response format: expected a list of tasks.")
            
            tasks = [TaskInfo(**kwargs) for kwargs in api_response.result]
        result.extend(tasks)

    return result

async def get_task_list_with_param(project_id: str, task_query: TaskQueryParam) -> list[TaskInfo]:
    async with DoorayApiClient.default_client() as client:
        response:httpx.Response = await client.get(f'{PROJECT_URL}/{project_id}/posts', params=task_query.model_dump(by_alias=True, exclude_none=True))
        api_response = ApiResponse(**response.json())

        if api_response.result is None or not isinstance(api_response.result, list):
            raise ValueError("Invalid response format: expected a list of tasks.")
        
        tasks = [TaskInfo(**kwargs) for kwargs in api_response.result]

    return tasks

async def get_detail_of_task(project_id: str, post_id: str):
    async with DoorayApiClient.default_client() as client:
        response = await client.get(f'{PROJECT_URL}/{project_id}/posts/{post_id}')
        logger.info(response)
        api_response = ApiResponse(**response.json())

        if api_response.result is None or not isinstance(api_response.result, dict):
            raise ValueError("Invalid response format: expected a dictionary for task detail.")

        result = TaskDetail(**api_response.result)

    return result

async def get_detail_of_task_by_id(post_id: str):
    """
    post_id만으로 업무 상세 정보를 조회합니다.
    두레이 URL (예: https://nhnent.dooray.com/project/tasks/1234567890)에서
    업무 ID를 추출하여 사용할 수 있습니다.
    """
    async with DoorayApiClient.default_client() as client:
        response = await client.get(f'{POST_URL}/{post_id}')
        logger.info(response)
        api_response = ApiResponse(**response.json())

        if api_response.result is None or not isinstance(api_response.result, dict):
            raise ValueError("Invalid response format: expected a dictionary for task detail.")

        result = TaskDetail(**api_response.result)

    return result

# ============ 업무 전체 상세 조회 (Full Detail) ============

async def get_full_detail_of_task(project_id: str, post_id: str) -> TaskFullDetail:
    """
    업무의 전체 상세 정보를 조회합니다.
    워크플로우, 담당자, 참조자, 태그, 마일스톤, 첨부파일 등 모든 정보를 포함합니다.
    """
    async with DoorayApiClient.default_client() as client:
        response = await client.get(f'{PROJECT_URL}/{project_id}/posts/{post_id}')
        logger.info(response)
        api_response = ApiResponse(**response.json())

        if api_response.result is None or not isinstance(api_response.result, dict):
            raise ValueError("Invalid response format: expected a dictionary for task detail.")

        result = TaskFullDetail(**api_response.result)

    return result

async def get_full_detail_of_task_by_id(post_id: str) -> TaskFullDetail:
    """
    post_id만으로 업무의 전체 상세 정보를 조회합니다.
    워크플로우, 담당자, 참조자, 태그, 마일스톤, 첨부파일 등 모든 정보를 포함합니다.

    두레이 URL (예: https://nhnent.dooray.com/project/tasks/1234567890)에서
    업무 ID를 추출하여 사용할 수 있습니다.
    """
    async with DoorayApiClient.default_client() as client:
        response = await client.get(f'{POST_URL}/{post_id}')
        logger.info(response)
        api_response = ApiResponse(**response.json())

        if api_response.result is None or not isinstance(api_response.result, dict):
            raise ValueError("Invalid response format: expected a dictionary for task detail.")

        result = TaskFullDetail(**api_response.result)

    return result

async def create_task(req: dict, project_id:str) -> httpx.Response:
    async with DoorayApiClient.default_client() as client:
        response = await client.post(f'{PROJECT_URL}/{project_id}/posts',
                                   content=CreateTask(**req).model_dump_json(by_alias=True))
    return response

async def upload_file_to_task(project_id: str, post_id: str, file_path: str) -> str:
    async with DoorayApiClient.default_client() as client:
        response: str = await client.redirect_post_with_file(f'{PROJECT_URL}/{project_id}/posts/{post_id}/files', file_path=file_path)
    return response

async def modify_task(project_id: str, post_id: str, modify: ModifyTask) -> httpx.Response:
    async with DoorayApiClient.default_client() as client:
        response = await client.put(f'{PROJECT_URL}/{project_id}/posts/{post_id}', content=modify.model_dump_json(by_alias=True))
    return response

# ============ 업무 상태 변경 관련 API ============

async def set_post_workflow(project_id: str, post_id: str, workflow_id: str) -> httpx.Response:
    """
    업무의 상태(워크플로우)를 변경합니다.
    업무 전체의 상태를 변경하며, 모든 담당자의 상태가 함께 변경됩니다.
    """
    import json
    async with DoorayApiClient.default_client() as client:
        response = await client.post(
            f'{PROJECT_URL}/{project_id}/posts/{post_id}/set-workflow',
            content=json.dumps({"workflowId": workflow_id})
        )
    return response

async def set_post_done(project_id: str, post_id: str) -> httpx.Response:
    """
    업무를 완료 상태로 변경합니다.
    완료 클래스 내의 대표 상태로 변경되며, 모든 담당자의 상태가 완료로 변경됩니다.
    """
    async with DoorayApiClient.default_client() as client:
        response = await client.post(f'{PROJECT_URL}/{project_id}/posts/{post_id}/set-done')
    return response

# ============ 업무 댓글 관련 API ============

async def get_post_comments(project_id: str, post_id: str, page: int = 0, size: int = 20, order: str = "createdAt") -> httpx.Response:
    """업무의 댓글 목록을 조회합니다."""
    async with DoorayApiClient.default_client() as client:
        response = await client.get(
            f'{PROJECT_URL}/{project_id}/posts/{post_id}/logs',
            params={"page": page, "size": size, "order": order}
        )
    return response

async def create_post_comment(project_id: str, post_id: str, content: str, mime_type: str = "text/x-markdown") -> httpx.Response:
    """업무에 댓글을 생성합니다."""
    import json
    body = {
        "body": {
            "content": content,
            "mimeType": mime_type
        }
    }
    async with DoorayApiClient.default_client() as client:
        response = await client.post(
            f'{PROJECT_URL}/{project_id}/posts/{post_id}/logs',
            content=json.dumps(body)
        )
    return response

async def update_post_comment(project_id: str, post_id: str, log_id: str, content: str, mime_type: str = "text/x-markdown") -> httpx.Response:
    """업무의 댓글을 수정합니다. 이메일로 발송된 댓글은 수정할 수 없습니다."""
    import json
    body = {
        "body": {
            "content": content,
            "mimeType": mime_type
        }
    }
    async with DoorayApiClient.default_client() as client:
        response = await client.put(
            f'{PROJECT_URL}/{project_id}/posts/{post_id}/logs/{log_id}',
            content=json.dumps(body)
        )
    return response

async def delete_post_comment(project_id: str, post_id: str, log_id: str) -> httpx.Response:
    """업무의 댓글을 삭제합니다."""
    async with DoorayApiClient.default_client() as client:
        response = await client.delete(f'{PROJECT_URL}/{project_id}/posts/{post_id}/logs/{log_id}')
    return response