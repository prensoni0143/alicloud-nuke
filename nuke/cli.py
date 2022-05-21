import click

from nuke.ali.base import Command
from nuke.registry import command_registry


@click.command()
@click.option('-r', '--resource-type', prompt='resource-type to list/delete',
              help='resource type.', type=click.Choice(list(command_registry.keys())), multiple=True)
@click.option('--delete', flag_value=True, default=False,
              help='delete resources.')
def nuke(resource_type, delete):
    """Simple program that greets NAME for a total of COUNT times."""
    print(f"resource-type: {resource_type}")
    print(f"delete       : {delete}")

    for cmd_name in resource_type:
        cmd: Command = command_registry.get(cmd_name)
        cmd.list()
        if delete:
            cmd.delete()


if __name__ == '__main__':
    nuke()
