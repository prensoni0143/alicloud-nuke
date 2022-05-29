import click

from nuke import service
from nuke.registry import command_registry
from nuke.service import resources_list


@click.command()
@click.option("--resource-type", "-r", type=click.Choice(list(command_registry.keys())),
              multiple=True, default=[], help="resource type.")
@click.option("--all", "all_resources", flag_value=True, default=False,
              help="include all support resources.")
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
        print("\nCommend has '--delete' option")
        confirm_deletion()
        service.delete_resources(targets)


def confirm_deletion():
    total = 0
    for k, v in resources_list.items():
        if len(v) > 0:
            print(f"Total No. of {k} to delete: {len(v)}")
            total = total + len(v)
    val = input(
        f"Total No. of resources to delete {total}: are you sure? (Y/N)")

    if val.lower() != "y":
        exit()
    else:
        return


if __name__ == "__main__":
    nuke()
