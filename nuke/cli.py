import click

from nuke import service
from nuke.registry import command_registry


@click.command()
@click.option("--resource-type", "-r", prompt="resource-type to list/delete",
              help="resource type.", type=click.Choice(list(command_registry.keys())), multiple=True)
@click.option("--all", "all_resources", flag_value=True, default=False, help="include all support resources.")
@click.option("--delete", flag_value=True, default=False,
              help="delete resources.")
def nuke(resource_type, all_resources, delete):
    """Ali Cloud Nuker. List/Delete target resources"""
    if all_resources:
        targets = list(command_registry.keys())
    else:
        targets = list(resource_type)

    print(f"target resource types are: {targets}")
    service.list_resources(targets)

    if delete:
        service.delete_resources(targets)


if __name__ == "__main__":
    nuke()
