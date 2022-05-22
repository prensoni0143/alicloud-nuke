from nuke.ali.base import Command
from nuke.ali.switch import Switch
from nuke.ali.util import regional_clients_registry
from nuke.ali.vpc import VPC


def main():
    for region_id, client in regional_clients_registry.items():
        # process_resource(region_id=region_id, resoruce=VPC(client))
        process_resource(region_id=region_id, resoruce=Switch(client))


def process_resource(region_id: str, resoruce: Command):
    # print(f"list {resoruce.name} in {region_id}")
    items = resoruce.list()
    if items:
        print(items)


if __name__ == '__main__':
    main()
