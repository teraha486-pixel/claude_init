import httpx
from model.dooray import ApiResponse
from utils.logger import logger

class DOORAY_HEADER:
    ORGANIZATION_MEMBER_ID = 'X-Om-Id'
    TENANT_ID = 'X-Tnt-Id'
    ORGANIZATION_ID= 'X-Org-Id'

class DoorayApiTokenContainer:
    __instance = None

    def __new__(cls, dooray_token):
        if cls.__instance is None:
            """creating singleton instance..."""
            cls.__instance = super(DoorayApiTokenContainer, cls).__new__(cls)
            cls.__instance.token = dooray_token #type: ignore
            cls.__instance.header = { #type: ignore
                'Authorization': f'dooray-api {cls.__instance.token}', #type: ignore
                'Content-Type': 'application/json'
            }
            return cls.__instance

    @classmethod
    def get_instance(cls):
        return cls.__instance

    @classmethod
    def get_token(cls) -> str:
        if cls.__instance is not None:
            return cls.__instance.token #type: ignore
        else:
            raise DoorayApiTokenContainer.TokenNotAvailableException

    class TokenNotAvailableException(Exception):
        def __init__(self):
            super().__init__('Dooray Open Api Token does not exist on mcp server')

class DoorayAsyncClient(httpx.AsyncClient):

    class DoorayApiClientException(Exception):
        def __init__(self, message: str, status_code: int):
            super().__init__(f'DoorayAsyncClient had an error: {message} with status code: {status_code}')

    def __init__(self, *args, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        if 'Authorization' not in kwargs.get('headers', {}):
            kwargs['headers']['Authorization'] = f'dooray-api {DoorayApiTokenContainer.get_token()}'
        super().__init__(*args, **kwargs)

    async def request(self, *args, **kwargs) -> httpx.Response:
        response = await super().request(*args, **kwargs)
        logger.debug(f'[{self.__class__.__name__}] response: {response.status_code} {response.text}')
        return response
    
    async def redirect_post_with_file(self, url: str, file_path: str, data: dict[str, str]={}) -> str:
        response = await self.post(url)

        if response.status_code in (301, 302, 303, 307, 308):
            redirect_url = response.headers.get('location')
            # Send both files and form data in the same request
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.split('/')[-1], f)}
                async with self.stream("POST", redirect_url, files=files, data=data) as response:
                    # return body as string
                    return (await response.aread()).decode('utf-8')

            # response = await self.post(redirect_url, files=files, data=data)
        else:
            raise self.DoorayApiClientException('File upload redirect was not found.', response.status_code)

        return response

class DoorayApiClient:
    @classmethod
    def default_client(cls):
        return DoorayAsyncClient(headers={
            'Authorization': f'dooray-api {DoorayApiTokenContainer.get_token()}',
            'Content-Type': 'application/json'
        })

    @classmethod
    def file_upload_client(cls):
        return DoorayAsyncClient(headers={
            'Authorization': f'dooray-api {DoorayApiTokenContainer.get_token()}'
        })

# class DoorayApiClientTest(httpx.AsyncClient):
#     def __init__(self, *args, **kwargs):
#         if 'headers' not in kwargs:
#             kwargs['headers'] = {}
#         if 'Content-Type' not in kwargs.get('headers', {}):
#             kwargs['headers']['Content-Type'] = 'application/json'
#         if 'Authorization' not in kwargs.get('headers', {}):
#             kwargs['headers']['Authorization'] = f'dooray-api {DoorayApiTokenContainer.get_token()}'
#         super().__init__(*args, **kwargs)

#     async def get(self, url, *args, **kwargs) -> ApiResponse:
#         response = await super().get(url, *args, **kwargs)
#         api_response = ApiResponse(**response.json())
#         return api_response
        