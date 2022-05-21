from typing import Dict

from nuke.ali.base import Command
from nuke.ali.ecs import ECS
from nuke.ali.vpc import VPC

command_registry: Dict[str, Command] = {}


def register_command(name, instance):
    command_registry[name] = instance


register_command("ecs", ECS())
register_command("vpc", VPC())
