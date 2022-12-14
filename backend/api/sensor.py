from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends

from backend.db.models import Sensor
from backend.service.exceptions import Error
from backend.service.sensor import SensorService

sensor_router = APIRouter()


@sensor_router.post('/sensor', response_model=None, responses={'400': {'model': Error}})
async def create_sensor(body: Sensor, service: SensorService = Depends()) -> Union[None, Error]:
	return await service.create(body)


@sensor_router.get('/sensor/{id}', response_model=Sensor, responses={'400': {'model': Error}})
async def get_sensor(id: UUID, service: SensorService = Depends()) -> Union[None, Error]:
	return await service.get(id)
