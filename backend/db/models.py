from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4

from sqlalchemy import Column, Integer, Text
from sqlmodel import SQLModel, Field, Relationship
from sqlmodel.sql.sqltypes import GUID


class SensorType(int, Enum):
	HUMIDITY = 0
	HEAT = 1


class OperatingMode(int, Enum):
	LOW = 0
	MEDIUM = 1
	HARD = 2


class Zone(int, Enum):
	A = 0
	B = 1
	C = 2
	D = 3


class Sensor(SQLModel, table=True):
	id: UUID = Field(sa_column=Column(GUID, as_uuid=True, primary_key=True, default=uuid4))
	name: str = Field(sa_column=Column(Text))
	type: SensorType
	zone: Zone
	sensor_info: List['SensorInfo'] = Relationship(back_populates="sensor")
	device: List['Device'] = Relationship(back_populates="sensor")
	max_value: int


class Device(SQLModel, table=True):
	id: UUID = Field(sa_column=Column(GUID, as_uuid=True, primary_key=True, default=uuid4))
	name: str = Field(sa_column=Column(Text))
	is_active: bool
	zone: Zone
	operating_mode: OperatingMode
	sensor_id: Optional[UUID] = Field(foreign_key="sensor.id")
	sensor: Sensor = Relationship(back_populates="device")


class SensorInfo(SQLModel, table=True):
	id: int = Field(sa_column=Column(Integer, autoincrement=True, primary_key=True))
	datetime: datetime
	sensor_id: Optional[UUID] = Field(foreign_key="sensor.id")
	sensor: Sensor = Relationship(back_populates="sensor_info")
	data: int
