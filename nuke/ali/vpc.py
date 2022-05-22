import json
from typing import List

from aliyunsdkvpc.request.v20160428 import DescribeRegionsRequest
from nuke.ali.base import Command


class VPC(Command):
    def list(self):
        print("list vpc")

    def delete(self):
        print("delete vpc")

    def list_regions(self) -> List[str]:
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        response = self.client.do_action_with_exception(request)
        data = json.loads(response.decode("UTF-8"))
        regions = [x.get("RegionId")
                   for x in data.get("Regions", {}).get("Region", [])]
        return regions
