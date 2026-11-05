#!/usr/bin/env python3
"""Regenerate, validate, build and package the current Studio delivery."""
from pathlib import Path
import shutil
import subprocess
import sys

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
filename = 'OP-Empire-Wars-Map-v0.2.rbxlx'
subprocess.run([rojo, 'build', 'default.project.json', '-o', f'build/{filename}'], cwd=root, check=True)
shutil.copy2(root/'build'/filename, root/'studio'/filename)
print(f'Livraison Studio : studio/{filename}')
