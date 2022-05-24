import json
from typing import Dict, List

from aliyunsdkvpc.request.v20160428 import (DescribeRegionsRequest,
                                            DescribeVpcsRequest)
from nuke.ali.base import Command


class VPC(Command):
    name = "vpc"
    display_name = "Virtual Private Cloud"

    def list(self) -> List[Dict[str, str]]:
        results = []
        page_count = 0
        total_count = -1

        while total_count > self.PAGE_SIZE * page_count or total_count == -1:
            page_count = page_count + 1
            request = DescribeVpcsRequest.DescribeVpcsRequest()
            request.set_PageSize(self.PAGE_SIZE)
            request.set_PageNumber(page_count)

            response: bytes = self.client.do_action_with_exception(request)
            r_json = json.loads(response.decode("UTF-8"))
            total_count = r_json.get("TotalCount")
            data = r_json.get("Vpcs", {}).get("Vpc", [])

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
