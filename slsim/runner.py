from fipy.docker import DockerCompose

from slsim.fiware import wait_on_orion, create_subscriptions
from slsim.sampler import WearableSampler, WorkerSampler


def bootstrap(docker: DockerCompose):
    docker.build_images()
    docker.start()

    wait_on_orion()
    create_subscriptions()


def send_entities():
    try:
        # todo run multiple Samplers in parallel
        WorkerSampler(pool_size=1).sample(samples_n=1, sampling_rate=1.0)  # label perceived fatigue
        WearableSampler(pool_size=1).sample(samples_n=10, sampling_rate=1.0)  # collect data for 5 minutes
    except Exception as e:
        print(e)


def run(env: str):
    services_running = False
    docker = DockerCompose(__file__,
                           docker_compose_file_name=f'docker-compose-{env}.yml',
                           docker_compose_cmd=['docker-compose'])
    try:
        bootstrap(docker)
        services_running = True

        print('>>> sending entities to Orion...')
        while True:
            send_entities()

    except KeyboardInterrupt:
        if services_running:
            docker.stop()
