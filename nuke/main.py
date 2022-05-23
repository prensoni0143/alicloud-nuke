from nuke.ali.base import Command
from nuke.registry import command_registry, regional_clients_registry


def main():
    for resource_name in ["vpc", "switch"]:
        for region_id, client in regional_clients_registry.items():
            resource: Command = command_registry.get(resource_name)
            if resource:
                process_resource(region_id=region_id,
                                 resoruce=resource(client))


def process_resource(region_id: str, resoruce: Command):
    items = resoruce.list()
    if items:
        print(items)


if __name__ == '__main__':
    main()
