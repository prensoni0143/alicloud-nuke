import csv
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from time import sleep
from typing import Dict, List

from aliyunsdkcore.client import AcsClient
from tabulate import tabulate

from nuke.ali.base import Command
from nuke.ali.oss import OSS
from nuke.registry import command_registry, regional_clients_registry

now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

ROOT = os.path.dirname(os.path.abspath(__file__))

def main():
    print(now)
    for resource_name in ["snapshot", "ecs", "disk", "sg", "switch", "vpc"]:
        # for region_id, client in regional_clients_registry.items():
        #     resource_class: type = command_registry.get(resource_name)
        #     # if resource_class and region_id in ["us-east-1", "cn-qingdao", "cn-zhangjiakou"] or True:
        #     if resource_class and region_id in ["us-east-1"]:
        #         resource = resource_class(client)
        #         process_resource(region_id=region_id, resource=resource)
        # sleep(5)

        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(list_resource_in_region, resource_name, region_id, client)
                       for region_id, client in regional_clients_registry.items()]

            for future in futures:
                tmp = future.result()
                results.extend(tmp)

        print("\nTotal No. of {display_name} ({name}): {number}".format(
            name=resource_name, display_name=command_registry.get(resource_name).display_name, number=len(results)))


def list_resource_in_region(resource_name: str, region_id: str, client: AcsClient) -> List[Dict[str, str]]:
    # print(f"list {resource_name} in {region_id}")
    resource_class: type = command_registry.get(resource_name)
    if not resource_class:
        raise ValueError(f"does not support resource: {resource_name}")
    resource = resource_class(client)

    items = resource.list()
    # print("{name} ({display_name}): {number}".format(
    #     name=resource.name, display_name=resource.display_name, number=len(items)))
    return items


def process_resource(region_id: str, resource: Command):
    items = resource.list()
    print(resource.display_name)
    if items:
        print(len(items))
        print(items)

    # for data in items:
    #     resource.delete(data=data)


if __name__ == '__main__':
    main()
