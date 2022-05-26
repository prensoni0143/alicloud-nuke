import json
from typing import Dict, List

from aliyunsdkcore.acs_exception.exceptions import (ClientException,
                                                    ServerException)
from aliyunsdkecs.request.v20140526 import DescribeSecurityGroupsRequest, DeleteSecurityGroupRequest
from nuke.ali.base import Command


class SecurityGroup(Command):
    name = "sg"
    display_name = "Security groups"

    def list(self) -> List[Dict[str, str]]:
        results = []
        page_count = 0
        total_count = -1

        while total_count > self.PAGE_SIZE * page_count or total_count == -1:
            page_count = page_count + 1
            request = DescribeSecurityGroupsRequest.DescribeSecurityGroupsRequest()
            request.set_PageSize(self.PAGE_SIZE)
            request.set_PageNumber(page_count)

            response: bytes = self.client.do_action_with_exception(request)
            r_json = json.loads(response.decode("UTF-8"))
            total_count = r_json.get("TotalCount")
            data = r_json.get("SecurityGroups", {}).get("SecurityGroup", [])

            for x in data:
                results.append(
                    {
                        "SecurityGroupId": x.get("SecurityGroupId", ""),
                        "SecurityGroupName": x.get("SecurityGroupName", ""),
                        "VpcId": x.get("VpcId", ""),
                        "CreationTime": x.get("CreationTime", "")
                    }
                )
        return results

    def delete(self, data: Dict[str, str]):
        try:
            id = data.get("SecurityGroupId")
            name = data.get("SecurityGroupName")
            request = DeleteSecurityGroupRequest.DeleteSecurityGroupRequest()
            request.set_SecurityGroupId(id)

            print(f"delete security group: {id} ({name})")
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            print(f"failed to delete: {e}")
        except ClientException as e:
            print(f"failed to delete: {e}")
