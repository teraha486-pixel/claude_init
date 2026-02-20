import httpx
from io import BytesIO
from adapter.dooray import DoorayApiClient
from model.dooray import ApiResponse
from model.drive.response.drive import DriveBrief, DriveInfo

DRIVE_URL = "https://api.dooray.com/drive/v1/drives"

async def get_drive_list(query_string: str) -> list[DriveBrief]:
    async with DoorayApiClient.default_client() as client:
        response:httpx.Response = await client.get(f"{DRIVE_URL}?{query_string}")
    api_response = ApiResponse(**response.json())

    if api_response.result is None or not isinstance(api_response.result, list):
        raise ValueError("Invalid response format: expected a list of drives.")

    drives = [DriveBrief(**kwargs) for kwargs in api_response.result]
    return drives

async def get_folder_list(drive_id,query_string: str) -> list[DriveInfo]:

    async with DoorayApiClient.default_client() as client:
        response:httpx.Response = await client.get(f"{DRIVE_URL}/{drive_id}/files?{query_string}")
    api_response = ApiResponse(**response.json())

    if api_response.result is None or not isinstance(api_response.result, list):
        raise ValueError("Invalid response format: expected a list of folders.")

    folders_in_drive = [DriveInfo(**kwargs) for kwargs in api_response.result]
        
    return folders_in_drive

async def upload_file_to_drive(drive_id:str, parent_id: str, file_path: str) -> httpx.Response:
    with open(file_path, 'rb') as f:
        files = {'file': (file_path.split('/')[-1], f)}
        response = await post_with_redirect(f'{DRIVE_URL}/{drive_id}/files?parentId={parent_id}', files)
    return response

async def upload_stream_to_drive(drive_id:str, parent_id: str, file_name: str, content: str) -> httpx.Response:
    file = BytesIO(content.encode("utf-8"))
    files = {'file': (file_name, file)}
    response = await post_with_redirect(f'{DRIVE_URL}/{drive_id}/files?parentId={parent_id}', files)
    return response

async def post_with_redirect(url:str, files):
    async with DoorayApiClient.file_upload_client() as client:
        response = await client.post(url,
            files=files)
                
        if response.status_code in (301, 302, 303, 307, 308):
            redirect_url = response.headers.get("location")
            response = await client.post(
                redirect_url,
                files=files
            )

    return response