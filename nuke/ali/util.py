import os
from typing import List, Tuple

from aliyunsdkcore.client import AcsClient
from nuke.ali.vpc import VPC


def get_regions() -> List[str]:
    access_key, secret_key = get_credential_from_env()
    client = AcsClient(
        ak=access_key,
        secret=secret_key,
    )
    vpc = VPC(client=client)
    regions = vpc.list_regions()
    return regions

def get_credential_from_env() -> Tuple[str, str]:
    access_key = os.environ.get("ALICLOUD_ACCESS_KEY", None)
    secret_key = os.environ.get("ALICLOUD_SECRET_KEY", None)

    if not access_key:
        raise ValueError("environment variable ALICLOUD_ACCESS_KEY is required.")
    if not secret_key:
        raise ValueError("environment variable ALICLOUD_SECRET_KEY is required.")

    return (access_key, secret_key)

if __name__ == '__main__':
    print(get_regions())
