from fipy.docker import DockerCompose

from slsim.__main__ import send_entities
from slsim.fiware import wait_on_orion, create_subscriptions


def bootstrap(docker: DockerCompose):
    docker.build_images()
    docker.start()

    wait_on_orion()
    create_subscriptions()


def run(env: str):
    services_running = False
    docker = DockerCompose(__file__,
                           docker_compose_file_name=f'docker-compose-{env}.yml',
                           docker_compose_cmd=['docker', 'compose'])
    try:
        bootstrap(docker)
        services_running = True

        print(f'>>> ORION URL: localhost:1026')
        while True:
            send_entities(5, 300, 1.0)

    except KeyboardInterrupt:
        if services_running:
            docker.stop()
