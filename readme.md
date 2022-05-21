# Ali Cloud Nuker

```cmd
pyinstaller --onefile cli.py --name ali-cloud-nuke --clean

ali-cloud-nuke.exe --resource-type ecs --delete
ali-cloud-nuke --resource-type ecs --resource-type vpc --delete

cli.py --resource-type ecs --delete

cli.py --resource-type ecs --resource-type vpc  --delete
cli.py -r ecs -r vpc  --delete

```
