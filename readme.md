# Ali Cloud Nuker

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

## Build .exe CLI

```bash
# download dependencies
pip install -r requirements.txt

# build exe files
pyinstaller nuke/cli.py  --name ali-cloud-nuke --clean

set ALICLOUD_ACCESS_KEY=xxxxx
set ALICLOUD_SECRET_KEY=xxxxxxx

# ali-cloud-nuke folder contains all dependencies
# ali-cloud-nuke\ali-cloud-nuke.exe is the executable file
dist\ali-cloud-nuke\ali-cloud-nuke.exe --help
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
