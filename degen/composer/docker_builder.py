import yaml


class DockerBuilder:

    @staticmethod
    def build(selected_tools):

        services = {}
        volumes = {}
        networks = {}

        for tool in selected_tools:

            tool_services = tool.get_docker_services() or {}
            tool_volumes = tool.get_docker_volumes() or {}
            tool_networks = tool.get_docker_networks() or {}

            services.update(tool_services)
            volumes.update(tool_volumes)
            networks.update(tool_networks)

        if not services:
            # return empty minimal docker file
            return yaml.dump({
                "services": {}
            }, sort_keys=False)

        docker_compose = {
                    "services": {}
        }

        for service_name, config in services.items():

            # garante que todos serviços leiam .env
            config.setdefault("env_file", [".env"])

            docker_compose["services"][service_name] = config

        if volumes:
            docker_compose["volumes"] = volumes

        if networks:
            docker_compose["networks"] = networks

        return yaml.dump(docker_compose, sort_keys=False)