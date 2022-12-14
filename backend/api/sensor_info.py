from typing import Union

from fastapi import APIRouter, Depends

from backend.db.models import SensorInfo
from backend.service.exceptions import Error
from backend.service.sensor_info import SensorInfoService

sensor_info_router = APIRouter()


@sensor_info_router.post('/sensor_info', response_model=None, responses={'400': {'model': Error}})
async def create_sensor_info(body: SensorInfo, service: SensorInfoService = Depends()) -> Union[None, Error]:
	return await service.create(body)


@sensor_info_router.get('/sensor_info/{id}', response_model=SensorInfo, responses={'400': {'model': Error}})
async def get_sensor_info(id: int, service: SensorInfoService = Depends()) -> Union[None, Error]:
	return await service.get(id)
