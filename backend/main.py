from fastapi import FastAPI
from sqlmodel import SQLModel
from starlette.requests import Request
from starlette.responses import JSONResponse

from backend.api.sensor import sensor_router
from backend.api.sensor_info import sensor_info_router
from backend.db.config import engine
from backend.service.exceptions import NotFoundException

app = FastAPI()


app.include_router(sensor_info_router)
app.include_router(sensor_router)


@app.exception_handler(NotFoundException)
async def exception_handler(request: Request, exc: NotFoundException):
	return JSONResponse(
		status_code=400,
		content={"message": exc.body},
	)


# TODO Set alembic
@app.on_event("startup")
async def on_startup():
	async with engine.begin() as conn:
		await conn.run_sync(SQLModel.metadata.drop_all)
		await conn.run_sync(SQLModel.metadata.create_all)
