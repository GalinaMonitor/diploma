from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.db.config import get_session
from backend.service.exceptions import NotFoundException


class BaseService:
	def __init__(self, session: AsyncSession = Depends(get_session)):
		self.session = session
		self.model = None

	async def get(self, id):
		statement = select(self.model).where(self.model.id == id)
		results = await self.session.exec(statement)
		result = results.first()
		if not result:
			raise NotFoundException()
		return result

	async def create(self, data) -> None:
		new_model = self.model(**data.dict())
		self.session.add(new_model)
		await self.session.commit()
		return new_model
