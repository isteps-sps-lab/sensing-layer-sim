import os
from typing import Optional

from fipy.ngsi.orion import OrionClient

from slsim.fiware import orion_client
from slsim.sampler import WearableSampler


def send_entities(pool_size: int, samples_n: int, sampling_rate: float,
                  orion: Optional[OrionClient] = orion_client()):
    try:
        print(f'>>> sending {samples_n} entities ({pool_size}/{sampling_rate} s) ...')
        WearableSampler(pool_size, orion).sample(samples_n, sampling_rate)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    uri = os.getenv("ORION_URI")
    tenant = os.getenv("TENANT")
    it = int(os.getenv("ITERATIONS"))
    print(f'> ORION URL: {uri}')
    print(f'> ORION SVC: {tenant}')
    print(f'> ITERATIONS: {it if it >= 0 else "infinite"}')
    i = 0
    while it - i != 0:
        print(f'>>> ITERATION #{i+1}')
        send_entities(int(os.getenv('POOL_SIZE')),
                      int(os.getenv('SAMPLES_N')),
                      float(os.getenv('SAMPLING_RATE')),
                      orion_client(uri, tenant))
        i = i + 1
