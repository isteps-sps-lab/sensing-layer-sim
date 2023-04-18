from fipy.ngsi.headers import FiwareContext
from fipy.ngsi.orion import OrionClient
from fipy.ngsi.quantumleap import QuantumLeapClient
from fipy.wait import wait_for_orion, wait_for_quantumleap
import json
from typing import List, Optional
from uri import URI

ORION_EXTERNAL_BASE_URL = 'http://localhost:1026'
QUANTUMLEAP_INTERNAL_BASE_URL = 'http://quantumleap:8668'
QUANTUMLEAP_EXTERNAL_BASE_URL = 'http://localhost:8668'
QUANTUMLEAP_SUB = {
    "description": "Notify QuantumLeap of changes to any entity.",
    "subject": {
        "entities": [
            {
                "idPattern": ".*"
            }
        ]
    },
    "notification": {
        "http": {
            "url": f"{QUANTUMLEAP_INTERNAL_BASE_URL}/v2/notify"
        }
    }
}


def orion_client(uri: Optional[str] = ORION_EXTERNAL_BASE_URL,
                 service: Optional[str] = None,
                 service_path: Optional[str] = None,
                 correlator: Optional[str] = None) -> OrionClient:
    base_url = URI(uri)
    ctx = FiwareContext(service=service,
                        service_path=service_path,
                        correlator=correlator)
    return OrionClient(base_url, ctx)


def wait_on_orion():
    wait_for_orion(orion_client(), max_wait=20)


class SubMan:

    def __init__(self):
        self._orion = orion_client()

    def create_subscriptions(self) -> List[dict]:
        self._orion.subscribe(QUANTUMLEAP_SUB)
        return self._orion.list_subscriptions()


def create_subscriptions():
    print(
        f"Creating catch-all entities subscription for QuantumLeap.")

    man = SubMan()
    orion_subs = man.create_subscriptions()
    formatted = json.dumps(orion_subs, indent=4)

    print("Current subscriptions in Orion:")
    print(formatted)


def quantumleap_client() -> QuantumLeapClient:
    base_url = URI(QUANTUMLEAP_EXTERNAL_BASE_URL)
    ctx = FiwareContext()
    return QuantumLeapClient(base_url, ctx)


def wait_on_quantumleap():
    wait_for_quantumleap(quantumleap_client())
