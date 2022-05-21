import click


@click.command()
@click.option('-r', '--resource-type', prompt='resource-type to list/delete',
              help='resource type.')
@click.option('--delete', flag_value=True, default=False,
              help='delete resources.')
def nuke(resource_type, delete):
    """Simple program that greets NAME for a total of COUNT times."""
    print(f"resource-type: {resource_type}")
    print(f"delete       : {delete}")


if __name__ == '__main__':
    nuke()
