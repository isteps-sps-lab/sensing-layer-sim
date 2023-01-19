from datetime import datetime
from fipy.ngsi.entity import FloatAttr
from fipy.ngsi.orion import OrionClient
from fipy.sim.sampler import DevicePoolSampler
import random
from typing import Optional

from slsim.ngsy import *
from slsim.fiware import orion_client


def get_session(worker_id: str) -> WorkerSession:
    return WorkerSession(
        session=Session(
            start=Datetime(
                dateTime=datetime.now().isoformat(),
                format="iso",
                timezoneId="utc"),
            end=None),
        worker=Worker(workerId=worker_id,
                      description="a worker")
    )


def get_wearable_attrs(session: WorkerSession) -> WearableDeviceAttr:
    return WearableDeviceAttr.new(
        WearableDevice(
            name="wearable",
            description="a wearable",
            workerSession=session,
            wearableAccelerometer=WearableAccelerometer(
                x=random.uniform(0, 1),
                y=random.uniform(0, 1),
                z=random.uniform(0, 1)
            ),
            deviceProperties=DeviceProperties(properties={})
        )
    )


def get_wearable_entity(session: WorkerSession) -> WearableEntity:
    return WearableEntity(
        id='',
        wearableDevice=get_wearable_attrs(session),
        sessionId=TextAttr.new('urn:ngsi-ld:Session:1'),
        workerId=TextAttr.new('urn:ngsi-ld:Worker:1'),
        temperature=FloatAttr.new(random.uniform(30, 40)),  # temperature
        gsr=FloatAttr.new(random.uniform(-2, 2)),  # gsr
        heartRate=FloatAttr.new(random.uniform(80, 150)),  # hr
        rrInterval=FloatAttr.new(random.uniform(300, 500)),
        position=PositionAttr.new(Position(latitude=-.5, longitude=.5)),
        timestamp=DateTimeAttr(
            value=datetime.now().isoformat(),
            metadata=DateTimeMetadata(
                format=TextAttr(value='iso'),
                timezoneId=TextAttr(value='utc')
            )
        ),
        metadata={}  # if None, an exception occurs
    )


def get_worker_states() -> WorkerStatesAttribute:
    return WorkerStatesAttribute.new(
        WorkerStates(
            perceivedFatigue=PerceivedFatigue(
                level=FloatAttr.new(random.randint(0, 10)),
                timestamp=Datetime(
                    dateTime=datetime.now().isoformat(),
                    format="iso",
                    timezoneId="utc"
                ),
                comment=TextAttr.new('Sim comment')
            )
        )
    )


def get_worker_entity() -> WorkerEntity:
    return WorkerEntity(
        id='',
        workerStates=get_worker_states()
    )


class WearableSampler(DevicePoolSampler):

    def __init__(self, pool_size: int, orion: Optional[OrionClient] = None):
        super().__init__(pool_size, orion if orion else orion_client())
        self.session = get_session('urn:ngsi-ld:Worker:1')

    def new_device_entity(self) -> WearableEntity:
        return get_wearable_entity(self.session)


class WorkerSampler(DevicePoolSampler):
    def __init__(self, pool_size: int, orion: Optional[OrionClient] = None):
        super().__init__(pool_size, orion if orion else orion_client())

    def new_device_entity(self) -> WearableEntity:
        return get_worker_entity()
