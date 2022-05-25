from nuke.ali.base import Command


class OSS(Command):
    name = "oss"
    display_name = "Object Storage Service"

    def list(self):
        print("list oss")

    def delete(self, id):
        print("delete oss")
