from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends

from backend.db.models import Device
from backend.service.exceptions import Error
from backend.service.device import DeviceService

device_router = APIRouter()


@device_router.post('/device', response_model=None, responses={'400': {'model': Error}})
async def create_device(body: Device, service: DeviceService = Depends()) -> Union[None, Error]:
	return await service.create(body)


@device_router.get('/device/{id}', response_model=Device, responses={'400': {'model': Error}})
async def get_device(id: UUID, service: DeviceService = Depends()) -> Union[None, Error]:
	return await service.get(id)
