import random
from datetime import datetime, timezone

from fipy.sim.sampler import DevicePoolSampler

from slsim.ngsy import *


class WearableSampler(DevicePoolSampler):

    def make_device_entity(self, nid: int) -> BaseEntity:
        wearable = super().make_device_entity(nid)
        wearable.wearableDevice.value.workerSession.worker.workerId = f'urn:ngsi-ld:Worker:{nid}'
        wearable.workerId = TextAttr.new(f'urn:ngsi-ld:Worker:{nid}')
        wearable.sessionId = TextAttr.new(f'urn:ngsi-ld:Session:{nid}')
        return wearable

    def new_device_entity(self) -> WearableEntity:
        return WearableEntity(
            id='urn:ngsi-ld:Wearable:1',
            wearableDevice=WearableDeviceAttr.new(
                WearableDevice(
                    name="SimWearable",
                    description="a simulated wearable",
                    workerSession=WorkerSession(
                        session=Session(
                            start=Datetime(
                                dateTime=datetime.now(timezone.utc).isoformat(),
                                format="ISO",
                                timezoneId="UTC"),
                            end=None),
                        worker=Worker(workerId='urn:ngsi-ld:Worker:1',
                                      description="a worker")
                    ),
                    wearableAccelometer=WearableAccelerometer(
                        x=random.uniform(0, 1),
                        y=random.uniform(0, 1),
                        z=random.uniform(0, 1)
                    ),
                    deviceProperties=DeviceProperties(properties={})
                )
            ),
            sessionId=TextAttr.new('urn:ngsi-ld:Session:1'),
            workerId=TextAttr.new('urn:ngsi-ld:Worker:1'),
            temperature=FloatAttr.new(random.uniform(30, 40)),  # temperature
            gsr=FloatAttr.new(random.uniform(-2, 2)),  # gsr
            heartRate=FloatAttr.new(random.uniform(80, 150)),  # hr
            rrInterval=FloatAttr.new(random.uniform(300, 500)),
            position=PositionAttr.new(Position(latitude=-.5, longitude=.5)),
            timestamp=DateTimeAttr(
                value=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                metadata=DateTimeMetadata(
                    format=TextAttr(value='ISO'),
                    timezoneId=TextAttr(value='UTC')
                )
            ),
            metadata={}  # if None, an exception occurs
        )
