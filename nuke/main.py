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

ROOT = os.path.dirname(os.path.abspath(__file__))
now = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def main():
    for resource_name in ["snapshot", "ecs", "disk", "sg", "switch", "vpc"]:
        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(list_resource_in_region, resource_name, region_id, client)
                       for region_id, client in regional_clients_registry.items()]

            for future in futures:
                tmp = future.result()
                results.extend(tmp)
        pretty_print(resource_name, results)

        for data in results:
            region_id = data.get("RegionId")
            client = regional_clients_registry.get(region_id)
            resource = get_resource_class_instance(resource_name, client)
            resource.delete(data=data)

    for resource_name in ["oss"]:
        results = []
        if resource_name == "oss":
            client = regional_clients_registry.get("cn-qingdao")
            oss_cmd: OSS = command_registry.get("oss")(client)
            results = oss_cmd.list_bucket()
        pretty_print(resource_name, results)

        for item in results:
            oss_cmd.delete_bucket(item.get("BucketName"), item.get("BucketLocation"))


def pretty_print(resource_name: str, results: List[Dict]):
    print("\nTotal No. of {display_name} ({name}): {number}".format(
        name=resource_name,
        display_name=command_registry.get(resource_name).display_name,
        number=len(results))
    )
    print_tables(results)
    write_csv(f"{ROOT}/{resource_name}-{now}.csv", results)


def write_csv(file_name, results: List[Dict]):
    if len(results) == 0:
        return
    data = [x.values() for x in results]
    headers = results[0].keys()
    with open(file_name, 'w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(headers)
        writer.writerows(data)


def print_tables(results: List[Dict]):
    if len(results) == 0:
        return
    data = [x.values() for x in results]
    headers = results[0].keys()
    print(tabulate(data, headers=headers))


def list_resource_in_region(resource_name: str, region_id: str, client: AcsClient) -> List[Dict[str, str]]:
    # print(f"list {resource_name} in {region_id}")
    resource = get_resource_class_instance(resource_name, client)
    items = resource.list()
    return items


def get_resource_class_instance(resource_name: str, client: AcsClient) -> Command:
    resource_class: type = command_registry.get(resource_name)
    if not resource_class:
        raise ValueError(f"does not support resource: {resource_name}")
    resource = resource_class(client)
    return resource


if __name__ == '__main__':
    main()
