import json
from typing import Dict, List

from aliyunsdkcore.acs_exception.exceptions import (ClientException,
                                                    ServerException)
from aliyunsdkecs.request.v20140526 import (DescribeInstancesRequest,
                                            DeleteInstanceRequest)
from nuke.ali.base import Command


class ECS(Command):
    name = "ecs"
    display_name = "Elastic Compute Service"

    def list(self) -> List[Dict[str, str]]:
        results = []
        page_count = 0
        total_count = -1

        while total_count > self.PAGE_SIZE * page_count or total_count == -1:
            page_count = page_count + 1
            request = DescribeInstancesRequest.DescribeInstancesRequest()
            request.set_PageSize(self.PAGE_SIZE)
            request.set_PageNumber(page_count)

            response: bytes = self.client.do_action_with_exception(request)
            r_json = json.loads(response.decode("UTF-8"))
            total_count = r_json.get("TotalCount")
            data = r_json.get("Instances", {}).get("Instance", [])

            for x in data:
                results.append(
                    {
                        "InstanceId": x.get("InstanceId", ""),
                        "InstanceName": x.get("InstanceName", ""),
                        "Status": x.get("Status", ""),
                        "RegionId": x.get("RegionId", ""),
                        "CreationTime": x.get("CreationTime", "")
                    }
                )
        return results

    def delete(self, data: Dict[str, str]):
        try:
            id = data.get("InstanceId")
            name = data.get("InstanceName")
            request = DeleteInstanceRequest.DeleteInstanceRequest()
            request.set_InstanceId(id)
            request.set_Force(True)

            print(f"deleting {self.name}: {id} ({name})")
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            return response_json
        except ServerException as e:
            print(f"client exception: failed to delete: {e}")
        except ClientException as e:
            print(f"server exception: failed to delete: {e}")
