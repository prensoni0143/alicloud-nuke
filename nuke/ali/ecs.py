from nuke.ali.base import Command


class ECS(Command):
    name = "ecs"
    display_name = "Elastic Compute Service"

    def list(self):
        print("list ecs")

    def delete(self):
        print("delete ecs")
