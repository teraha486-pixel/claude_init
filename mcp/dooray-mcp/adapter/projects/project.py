from typing import Any
import httpx
from adapter.dooray import DoorayApiClient
from model.dooray import ApiResponse
from model.projects.response.project import ProjectInfo, MilestoneInfo, TagInfo

PROJECT_URL = "https://api.dooray.com/project/v1/projects"

async def get_my_project_list(project_type: str, **kwargs) -> list[ProjectInfo]:
    # 내가 속한 프로젝트의 목록을 가져오도록 함.
    # 나중에 내가 속하지 않은 프로젝트의 리스트도 가져와야 할 소요가 있다면, 이 항목을 수정하면 가능.
    kwargs['member'] = 'me'
    kwargs['type'] = project_type

    # scope 를 private 으로 지정합니다.
    # private 으로 지정하면, 프로젝트의 공개 여부가 모두 멤버로 한정된 프로젝트만 가져오고,
    # public 으로 지정되면, 공개여부가 하나라도 공개되어 있다면 모두 가져오게 됩니다.
    # NOTE: 현재 scope 를 private/public 으로 나누는 분기를 설정하기 어려운 상태이므로 private 으로 고정하고 있습니다.
    #  따라서 현재는 사용자에 따라 public 으로 수정하여 사용해야 합니다.
    kwargs['scope'] = 'private'

    async with DoorayApiClient.default_client() as client:
        response: httpx.Response = await client.get(PROJECT_URL, params=kwargs)
    api_response = ApiResponse(**response.json())

    if api_response.result is not None and isinstance(api_response.result, list):
        projects = [ProjectInfo(**kw) for kw in api_response.result]
        return projects
    else:
        raise ValueError("Invalid response format: expected a list of projects.")

async def get_project_milestones(project_id: str, page: int, size: int, status: str) -> list[MilestoneInfo]:
    async with DoorayApiClient.default_client() as client:
        response: httpx.Response = await client.get(f'{PROJECT_URL}/{project_id}/milestones', params={
            'page': page,
            'size': size,
            'status': status
        })
    api_response = ApiResponse(**response.json())

    if api_response.result is not None and isinstance(api_response.result, list):
        milestones = [MilestoneInfo(**kw) for kw in api_response.result]
        return milestones
    else:
        raise ValueError("Invalid response format: expected a list of milestones.")

async def get_project_tags(project_id: str, page: int, size: int) -> list[TagInfo]:
    async with DoorayApiClient.default_client() as client:
        response: httpx.Response = await client.get(f'{PROJECT_URL}/{project_id}/tags', params={
            'page': page,
            'size': size
        })
    api_response = ApiResponse(**response.json())

    if api_response.result is not None and isinstance(api_response.result, list):
        tags = [TagInfo(**kw) for kw in api_response.result]
        return tags
    else:
        raise ValueError("Invalid response format: expected a list of tags.")