from nuke.ali.vpc import VPC

from nuke.ali.util import regional_clients_registry


def main():
    for region_id, client in regional_clients_registry.items():
        vpc = VPC(client=client)
        print(f"process {region_id}")
        print(vpc.list())


if __name__ == '__main__':
    main()
