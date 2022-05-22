import json
from typing import Dict, List

from aliyunsdkvpc.request.v20160428 import (DescribeRegionsRequest,
                                            DescribeVpcsRequest)
from nuke.ali.base import Command


class VPC(Command):
    name = "vpc"
    display_name = "Virtual Private Cloud"

    def list(self) -> List[Dict[str, str]]:
        request = DescribeVpcsRequest.DescribeVpcsRequest()
        request.set_PageSize = 10
        request.set_PageNumber = 1

        response: bytes = self.client.do_action_with_exception(request)
        data = json.loads(
            response.decode("UTF-8")).get("Vpcs", {}).get("Vpc", [])

        results = []
        for x in data:
            results.append(
                {
                    "VpcId": x.get("VpcId"),
                    "VpcName": x.get("VpcName"),
                    "RegionId": x.get("RegionId"),
                    "CreationTime": x.get("CreationTime")
                }
            )
        return results

    def delete(self):
        print("delete vpc")

    def list_regions(self) -> List[str]:
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        response: bytes = self.client.do_action_with_exception(request)

        data = json.loads(response.decode("UTF-8")
                          ).get("Regions", {}).get("Region", [])
        regions = [x.get("RegionId") for x in data]

        return regions
