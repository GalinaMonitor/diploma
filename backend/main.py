from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from backend.api.device import device_router
from backend.api.sensor import sensor_router
from backend.api.sensor_info import sensor_info_router
from backend.service.exceptions import NotFoundException

app = FastAPI()


app.include_router(sensor_info_router)
app.include_router(sensor_router)
app.include_router(device_router)


@app.exception_handler(NotFoundException)
async def exception_handler(request: Request, exc: NotFoundException):
	return JSONResponse(
		status_code=400,
		content={"message": exc.body},
	)
