from nuke.ali.base import Command
from nuke.registry import command_registry, regional_clients_registry


def main():
    for resource_name in ["vpc", "switch"]:
        for region_id, client in regional_clients_registry.items():
            resource_class: type = command_registry.get(resource_name)
            if resource_class and region_id in ["cn-qingdao", "cn-zhangjiakou"]:
                resource = resource_class(client)
                process_resource(region_id=region_id, resource=resource)


def process_resource(region_id: str, resource: Command):
    items = resource.list()
    if items:
        print(len(items))
        print(items)

    for data in items:
        resource.delete(data=data)
    
    # for data in items:
    #     id = "vsw-m5e3m6icclgmuprwl3b1d"
    #     if x.get("VSwitchId") == id:
    #         resource.delete(data=data)
    
    # for data in items:
    #     id = "vpc-m5egw68q0uzjlw3xi4ye1"
    #     if x.get("VpcId") == id:
    #         resource.delete(data=data)


if __name__ == '__main__':
    main()
