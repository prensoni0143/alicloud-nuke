from datetime import datetime
from typing import Dict, List

import oss2
from nuke.ali.base import Command
from oss2.models import SimplifiedBucketInfo


class OSS(Command):
    name = "oss"
    display_name = "Object Storage Service"

    def list(self):
        raise NotImplementedError(
            "OSS bucket has different API, as it is Global. Please use list_bucket() method.")

    def list_bucket(self) -> List[Dict[str, str]]:
        access_key = self.client.get_access_key()
        access_secret = self.client.get_access_secret()
        region_id = self.client.get_region_id()

        auth = oss2.Auth(access_key, access_secret)
        service = oss2.Service(auth, f'https://oss-{region_id}.aliyuncs.com')

        results = []

        # List all buckets that belong to the current Alibaba Cloud account.
        for b in oss2.BucketIterator(service, max_keys=50):
            b_info: SimplifiedBucketInfo = b
            #  This API returns timestamp (1653519957)
            #  while other APIs return time (2022-05-23T11:30:40Z).
            timestamp = b_info.creation_date
            create_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%dT%H:%M:%SZ")

            #  OSS does not have a bucket Id, as bucket name is global unique
            results.append(
                {
                    "BucketName": b_info.name,
                    "BucketLocation": b_info.location,
                    "CreationTime": create_time
                }
            )
        return results

    def delete(self, id):
        print("delete oss")
