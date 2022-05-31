# alicloud-nuke

This Repo is dedicated to development of Alibaba Cloud Nuke (Resource Deletion) project

The `ali-cloud-nuke` CLI supports 
- Delete all resources (6 to 8 that we cover)
- Delete a particular type of resource, such as `ecs`, `oss`, `vpc`.

To delete a resource, we need to delete its dependencies. We validated the following dependencies.
- empty `oss bucket objects`, then delete an `oss bucket`
- delete `ecs`, then `disk`, `sg`
- delete `switch`, `sg` then `vpc`

## Run ali-cloud-nuke CLI

```bash
# setup account access_key/secret_key
set ALICLOUD_ACCESS_KEY=xxxxx
set ALICLOUD_SECRET_KEY=xxxxxxx

# download dependencies
pip install -r requirements.txt

python -m nuke.cli --help
```

## Example CLI Commands

```bash
set ALICLOUD_ACCESS_KEY=xxxxx
set ALICLOUD_SECRET_KEY=xxxxxxx

# list all ecs resources
python -m nuke.cli --resource-type ecs

# list all ecs, oss resources
python -m nuke.cli -r ecs -r vpc

# list all resources
python -m nuke.cli --all

# delete ecs, oss resources
python -m nuke.cli -r ecs -r vpc --delete

# delete all resources
python -m nuke.cli --all --delete
```

## Run Terraform to provision resources

Provision of resources to test the deletion, and the dependencies.

```bash
# setup account access_key/secret_key
set ALICLOUD_ACCESS_KEY=xxxxx
set ALICLOUD_SECRET_KEY=xxxxxxx

# ensure Terraform cli in PATH
set PATH=C:\Tools\terraform\1.2.0;%PATH%

cd terraform\vpc
terraform init
terraform apply --auto-approve

```
