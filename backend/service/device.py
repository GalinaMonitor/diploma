from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.db.config import get_session
from backend.db.models import Device
from backend.service.base import BaseService


class DeviceService(BaseService):
	def __init__(self, session: AsyncSession = Depends(get_session)):
		super().__init__(session)
		self.model = Device

	async def get_from_sensor_id(self, id):
		statement = select(self.model).where(self.model.sensor_id == id)
		results = await self.session.exec(statement)
		result = results.all()
		return result
