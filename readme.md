# Ali Cloud Nuker

```cmd
pyinstaller --onefile nuke/cli.py --name ali-cloud-nuke --clean

ali-cloud-nuke.exe --resource-type ecs --delete
ali-cloud-nuke --resource-type ecs --resource-type vpc --delete

python -m nuke.cli --resource-type ecs --delete
python -m nuke.cli --resource-type ecs --resource-type vpc  --delete
python -m nuke.cli -r ecs -r vpc  --delete

```