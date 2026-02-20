import httpx
from adapter.dooray import DoorayApiClient
from model.messenger.request.message import Message, DirectMessage 
from model.dooray import ApiResponse
from model.messenger.response.channel import ChannelInfo

MESSENGER_PATH = 'https://api.dooray.com/messenger/v1'

async def send_message_directly(text: str, organization_member_id: str) -> httpx.Response:
    async with DoorayApiClient.default_client() as client:
        response = await client.post(f'{MESSENGER_PATH}/channels/direct-send', content=DirectMessage(
            text=text, organizationMemberId=organization_member_id
        ).model_dump_json(by_alias=True))
    return response

async def get_channels_belonged_to() -> list[ChannelInfo]:
    async with DoorayApiClient.default_client() as client:
        response = await client.get(f'{MESSENGER_PATH}/channels')
    api_response = ApiResponse(**response.json())

    if api_response.result is None or not isinstance(api_response.result, list):
        raise ValueError("Invalid response format: expected a list of channels.")

    return [ChannelInfo(**kwargs) for kwargs in api_response.result]

async def send_message_to_channel(channel_id: str, text: str) -> httpx.Response:
    async with DoorayApiClient.default_client() as client:
        response = await client.post(f'{MESSENGER_PATH}/channels/{channel_id}/logs', content=Message(
            text=text
        ).model_dump_json())
        return response

async def modify_message_sent_to_channel(channel_id: str, log_id: str, text: str) -> httpx.Response:
    async with DoorayApiClient.default_client() as client:
        response = await client.put(f'{MESSENGER_PATH}/channels/{channel_id}/logs/{log_id}', content=Message(
            text=text
        ).model_dump_json())
        return response

async def delete_message_sent_to_channel(channel_id: str, log_id: str) -> httpx.Response:
    async with DoorayApiClient.default_client() as client:
        response = await client.delete(f'{MESSENGER_PATH}/channels/{channel_id}/logs/{log_id}')
        return response
