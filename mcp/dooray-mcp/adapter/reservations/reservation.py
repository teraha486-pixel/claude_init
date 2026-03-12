from adapter.dooray import DoorayApiClient

RESERVATION_PATH = 'https://api.dooray.com/reservation/v1'


async def get_resource_categories(size: int = 20, page: int = 0):
    async with DoorayApiClient.default_client() as client:
        response = await client.get(f'{RESERVATION_PATH}/resource-categories', params={
            'size': size,
            'page': page
        })
    return response


async def get_resources(resource_category_id: str = None):
    params = {}
    if resource_category_id:
        params['resourceCategoryId'] = resource_category_id
    async with DoorayApiClient.default_client() as client:
        response = await client.get(f'{RESERVATION_PATH}/resources', params=params)
    return response


async def get_resource_detail(resource_id: str):
    async with DoorayApiClient.default_client() as client:
        response = await client.get(f'{RESERVATION_PATH}/resources/{resource_id}')
    return response


async def get_reservable_resources(resource_category_id: str = None):
    params = {}
    if resource_category_id:
        params['resourceCategoryId'] = resource_category_id
    async with DoorayApiClient.default_client() as client:
        response = await client.get(f'{RESERVATION_PATH}/reservable-resources', params=params)
    return response


async def get_resource_reservations(time_min: str, time_max: str, resource_ids: list[str] = None, size: int = 20, page: int = 0):
    params = {
        'timeMin': time_min,
        'timeMax': time_max,
        'size': size,
        'page': page
    }
    if resource_ids:
        params['resourceIds'] = ','.join(resource_ids)
    async with DoorayApiClient.default_client() as client:
        response = await client.get(f'{RESERVATION_PATH}/resource-reservations', params=params)
    return response


async def create_resource_reservation(body: dict):
    async with DoorayApiClient.default_client() as client:
        response = await client.post(f'{RESERVATION_PATH}/resource-reservations', json=body)
    return response


async def get_resource_reservation_detail(resource_reservation_id: str):
    async with DoorayApiClient.default_client() as client:
        response = await client.get(f'{RESERVATION_PATH}/resource-reservations/{resource_reservation_id}')
    return response


async def update_resource_reservation(resource_reservation_id: str, body: dict):
    async with DoorayApiClient.default_client() as client:
        response = await client.put(f'{RESERVATION_PATH}/resource-reservations/{resource_reservation_id}', json=body)
    return response


async def delete_resource_reservation(resource_reservation_id: str, delete_type: str = ''):
    body = {'deleteType': delete_type}
    async with DoorayApiClient.default_client() as client:
        response = await client.request('DELETE', f'{RESERVATION_PATH}/resource-reservations/{resource_reservation_id}', json=body)
    return response
