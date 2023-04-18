from typing import Dict, Optional

from fipy.ngsi.entity import BaseEntity, FloatAttr, TextAttr, Attr, BoolAttr
from pydantic import BaseModel


class Datetime(BaseModel):
    dateTime: str
    format: str
    timezoneId: str


class Session(BaseModel):
    start: Datetime
    end: Optional[Datetime]


class Worker(BaseModel):
    workerId: str
    description: str


class WorkerSession(BaseModel):
    session: Session
    worker: Worker


class DeviceProperties(BaseModel):
    properties: Dict


class WearableAccelerometer(BaseModel):
    x: float
    y: float
    z: float


class WearableDevice(BaseModel):
    name: str
    description: str
    workerSession: WorkerSession
    wearableAccelometer: WearableAccelerometer
    deviceProperties: DeviceProperties


class WearableDeviceAttr(Attr):
    type = 'StructuredValue'
    value: WearableDevice


class Position(BaseModel):
    latitude: float
    longitude: float


class PositionAttr(Attr):
    type = 'StructuredValue'
    value: Position


class DateTimeMetadata(BaseModel):
    format: TextAttr
    timezoneId: TextAttr


class DateTimeAttr(Attr):
    type = 'DateTime'
    value: str
    metadata: Optional[DateTimeMetadata]


class WearableEntity(BaseEntity):
    type = 'Wearable'
    wearableDevice: Optional[WearableDeviceAttr]
    workerId: Optional[TextAttr]
    sessionId: Optional[TextAttr]
    temperature: Optional[FloatAttr]
    gsr: Optional[FloatAttr]
    heartRate: Optional[FloatAttr]
    rrInterval: Optional[FloatAttr]
    position: Optional[PositionAttr]
    timestamp: Optional[DateTimeAttr]
    metadata: Optional[Dict]
