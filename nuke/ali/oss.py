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

    def delete(self, data: Dict[str, str]):
        raise NotImplementedError(
            "OSS bucket has different API, as it is Global. Please use delete_bucket() method.")

    def list_bucket(self) -> List[Dict[str, str]]:
        """unlick most resources, this method lists all the buckets in all regions.
        """
        region_id = self.client.get_region_id()
        auth = oss2.Auth(self.client.get_access_key(), self.client.get_access_secret())
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

    def delete_bucket(self, name:str, region_id:str):
        auth = oss2.Auth(self.client.get_access_key(), self.client.get_access_secret())
        bucket = oss2.Bucket(auth, f'https://oss-{region_id}.aliyuncs.com', name)

        try:
            # Delete the bucket.
            print(f"delete oss bucket: {name}")
            bucket.delete_bucket()
        except oss2.exceptions.BucketNotEmpty:
            print(f"error: bucket {name} is not empty.")
        except oss2.exceptions.NoSuchBucket:
            print(f"bucket {name} does not exist")
