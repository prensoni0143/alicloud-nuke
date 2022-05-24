import json
from typing import Dict, List

from aliyunsdkcore.acs_exception.exceptions import (ClientException,
                                                    ServerException)
from aliyunsdkvpc.request.v20160428 import (DeleteVSwitchRequest,
                                            DescribeVSwitchesRequest)
from nuke.ali.base import Command


class Switch(Command):
    name = "switch"
    display_name = "vSwitches"

    def list(self) -> List[Dict[str, str]]:
        results = []
        page_count = 0
        total_count = -1

        while total_count > self.PAGE_SIZE * page_count or total_count == -1:
            page_count = page_count + 1
            request = DescribeVSwitchesRequest.DescribeVSwitchesRequest()
            request.set_PageSize(self.PAGE_SIZE)
            request.set_PageNumber(page_count)

            response: bytes = self.client.do_action_with_exception(request)
            r_json = json.loads(response.decode("UTF-8"))
            total_count = r_json.get("TotalCount")
            data = r_json.get("VSwitches", {}).get("VSwitch", [])

            for x in data:
                results.append(
                    {
                        "VSwitchId": x.get("VSwitchId", ""),
                        "VSwitchName": x.get("VSwitchName", ""),
                        "ZoneId": x.get("ZoneId", ""),
                        "CreationTime": x.get("CreationTime", "")
                    }
                )
        return results

    def delete(self, id: str):
        try:
            request = DeleteVSwitchRequest.DeleteVSwitchRequest()
            # The ID of the vSwitch that you want to delete.
            request.set_VSwitchId(id)
            
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            # Check whether the vSwitch is deleted.
            # if self.check_status(self.TIME_DEFAULT_OUT, self.DEFAULT_TIME * 5,
            #                      self.describe_vswitch_status,
            #                      '', id):
            return response_json
        except ServerException as e:
            print(e)
        except ClientException as e:
            print(e)
