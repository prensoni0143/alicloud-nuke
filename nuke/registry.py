from typing import Dict, List

from aliyunsdkcore.client import AcsClient

from nuke.ali.base import Command
from nuke.ali.ecs import ECS
from nuke.ali.switch import Switch
from nuke.ali.util import get_regional_client, list_all_regions
from nuke.ali.vpc import VPC

command_registry: Dict[str, Command] = {}

regional_clients_registry: List[Dict[str, AcsClient]] = {}


def register_command(name, instance):
    command_registry[name] = instance


def register():
    # update global command_registry
    register_command(Switch.name, Switch)
    register_command(VPC.name, VPC)
    # register_command(ECS.name, ECS)

    # update global regional_clients_registry
    region_ids = list_all_regions()

    for region in region_ids:
        regional_clients_registry[region] = get_regional_client(region)


#  run register() method upon import registry module
register()
