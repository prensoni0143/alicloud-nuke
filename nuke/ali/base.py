from typing import Dict, List

from aliyunsdkcore.client import AcsClient


class Command:
    PAGE_SIZE = 5

    def __init__(self, client) -> None:
        self.client: AcsClient = client

    def list(self):
        pass

    def delete(self, data: Dict[str, str]):
        pass
