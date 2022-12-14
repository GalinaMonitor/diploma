from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.db.config import get_session
from backend.db.models import SensorInfo
from backend.service.base import BaseService


class SensorInfoService(BaseService):
	def __init__(self, session: AsyncSession = Depends(get_session)):
		super().__init__(session)
		self.model = SensorInfo
