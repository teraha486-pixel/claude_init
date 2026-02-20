import httpx
from adapter.dooray import DoorayApiClient, DOORAY_HEADER
from adapter.projects.project import PROJECT_URL
import json

COMMON_PATH = 'https://api.dooray.com/common/v1'

async def get_members_information_by_name(name: str, page: int, size: int) -> httpx.Response:
    async with DoorayApiClient.default_client() as client:
        response = await client.get(f'{COMMON_PATH}/members', params={'name': name, 'page': page, 'size': size})
    return response

async def get_my_member_identities() -> httpx.Response:
    async with DoorayApiClient.default_client() as client:
        response = await client.post(f'{PROJECT_URL}/is-creatable', content=json.dumps({'code': 'dooray'}))
        omid = response.headers[DOORAY_HEADER.ORGANIZATION_MEMBER_ID]
        response = await client.get(f'{COMMON_PATH}/members/{omid}')
    return response