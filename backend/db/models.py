from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from typing import Optional, List

from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import UUID as SQLUUID
from sqlmodel import SQLModel, Field, Relationship


class SensorType(int, Enum):
	HUMIDITY = 0
	HEAT = 1


class Zone(int, Enum):
	A = 0
	B = 1
	C = 2
	D = 3


class Sensor(SQLModel, table=True):
	id: UUID = Field(sa_column=Column(SQLUUID, primary_key=True, default=uuid4))
	type: SensorType
	zone: Zone
	sensor_info: List['SensorInfo'] = Relationship(back_populates="sensor")


class SensorInfo(SQLModel, table=True):
	id: int = Field(sa_column=Column(Integer, autoincrement=True, primary_key=True))
	datetime: datetime
	sensor_id: Optional[UUID] = Field(foreign_key="sensor.id")
	sensor: Sensor = Relationship(back_populates="sensor_info")
	data: int
