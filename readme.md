# Ali Cloud Nuker

The `ali-cloud-nuke` CLI supports 
- Delete all resources (6 to 8 that we cover)
- Delete a particular type of resources, such as `ecs`, `oss`, `vpc`.

## Run ali-cloud-nuke CLI

```bash
# setup account access_key/secret_key
set ALICLOUD_ACCESS_KEY=xxxxx
set ALICLOUD_SECRET_KEY=xxxxxxx

python -m nuke.cli --help
```

## Example CLI Commands

```bash
set ALICLOUD_ACCESS_KEY=xxxxx
set ALICLOUD_SECRET_KEY=xxxxxxx

# list all ecs resources
ali-cloud-nuke.exe --resource-type ecs

# list all ecs, oss resources
ali-cloud-nuke.exe -r ecs -r vpc

# list all resources
ali-cloud-nuke.exe --all

# delete ecs, oss resources
ali-cloud-nuke.exe -r ecs -r vpc --delete

# delete all resources
ali-cloud-nuke.exe --all --delete
```

## Run Terraform to provision resources

Provison a list of resources to test the deletion, and the dependencies.

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
