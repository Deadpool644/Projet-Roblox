#!/usr/bin/env python3
"""Regenerate, validate, build and package the current Studio delivery."""
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
rojo = shutil.which('rojo')
if rojo is None:
    cloud_binary = Path('/workspace/tooling/rojo-7.6.1/rojo')
    if cloud_binary.is_file():
        rojo = str(cloud_binary)
if rojo is None:
    sys.exit('Rojo introuvable. Installer Rokit puis lancer rokit install dans le projet.')
if subprocess.check_output([rojo, '--version'], text=True).strip() != 'Rojo 7.6.1':
    sys.exit('Utiliser Rojo 7.6.1, version épinglée dans rokit.toml.')
subprocess.run([sys.executable, 'tools/build_map.py'], cwd=root, check=True)
subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tools', '-p', 'test_*.py', '-v'], cwd=root, check=True)
(root/'build').mkdir(exist_ok=True)
(root/'studio').mkdir(exist_ok=True)
filename = 'OP-Empire-Wars-Map-v0.3.rbxlx'
subprocess.run([rojo, 'build', 'default.project.json', '-o', f'build/{filename}'], cwd=root, check=True)
place = ET.parse(root/'build'/filename)
model = place.getroot()  # A place XML stores services directly below <roblox>.


def instance_at(path):
    item = model
    for name in path:
        item = next((i for i in item.findall('Item') if i.find("Properties/string[@name='Name']").text == name), None)
        if item is None:
            sys.exit(f'Livraison incomplète : {"/".join(path)}')
    return item


assert instance_at(['StarterPlayer','StarterPlayerScripts','MaritimeWeather']).get('class') == 'LocalScript'
assert instance_at(['ReplicatedStorage','WorldEnvironment']).get('class') == 'ModuleScript'
assert instance_at(['Workspace','Terrain','MaritimeClouds']).get('class') == 'Clouds'
lighting = instance_at(['Lighting'])
for kind in ('Sky','Atmosphere'):
    assert len(lighting.findall(f"Item[@class='{kind}']")) == 1, f'{kind} absent ou dupliqué'
shutil.copy2(root/'build'/filename, root/'studio'/filename)
print(f'Livraison Studio : studio/{filename}')
