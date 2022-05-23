import json
from typing import Dict, List

from aliyunsdkvpc.request.v20160428 import DescribeVSwitchesRequest
from nuke.ali.base import Command


class Switch(Command):
    name = "switch"
    display_name = "vSwitches"

    def list(self) -> List[Dict[str, str]]:
        request = DescribeVSwitchesRequest.DescribeVSwitchesRequest()
        request.set_PageSize = 10
        request.set_PageNumber = 1

        response: bytes = self.client.do_action_with_exception(request)

        data = json.loads(
            response.decode("UTF-8")).get("VSwitches", {}).get("VSwitch", [])

        results = []
        for x in data:
            results.append({
                "VSwitchId": x.get("VSwitchId", ""),
                "VSwitchName": x.get("VSwitchName", ""),
                "ZoneId": x.get("ZoneId", ""),
                "CreationTime": x.get("CreationTime", "")
            })
        return results

    def delete(self):
        print("delete vpc")
