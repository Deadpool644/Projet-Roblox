"""Structural and layout checks. Roblox Studio playtests remain necessary."""
import collections
import json
import math
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class MapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = json.loads((ROOT / 'tools/world.json').read_text())
        cls.xml = ET.parse(ROOT / 'assets/Archipelago.rbxmx')
        cls.parts = [p for p in cls.xml.findall('.//Item') if p.get('class') in ('Part', 'SpawnLocation')]

    def test_catalogue_and_rings(self):
        islands = self.cfg['islands']
        self.assertEqual(len({i['id'] for i in islands}), 13)
        self.assertEqual(collections.Counter(i['tier'] for i in islands), {1: 4, 2: 5, 3: 4})
        radii = {t: [math.hypot(i['x'], i['z']) for i in islands if i['tier'] == t] for t in (1, 2, 3)}
        self.assertLess(max(radii[1]), min(radii[2]))
        self.assertLess(max(radii[2]), min(radii[3]))

    def test_coastlines_and_harbors_have_space(self):
        islands = [self.cfg['hub'], *self.cfg['islands']]
        for index, a in enumerate(islands):
            for b in islands[index+1:]:
                # Includes 110 extra studs per island for docks/coast, plus 100 navigation clearance.
                gap = math.hypot(a['x']-b['x'], a['z']-b['z'])-1.2*a['radius']-1.2*b['radius']-220
                self.assertGreater(gap, 100, (a['id'], b['id']))
            self.assertLess(max(abs(a['x']), abs(a['z']))+a['radius']+110, 3072)

    def test_static_geometry(self):
        for p in self.parts:
            props = p.find('Properties')
            self.assertEqual(props.find("bool[@name='Anchored']").text, 'true')
            size = [float(v.text) for v in props.find("Vector3[@name='size']")]
            self.assertTrue(all(v > 0 and math.isfinite(v) for v in size))
            frame = props.find("CoordinateFrame[@name='CFrame']")
            matrix = [[float(frame.find(f'R{i}{j}').text) for j in range(3)] for i in range(3)]
            for i in range(3):
                for j in range(3):
                    self.assertAlmostEqual(sum(matrix[i][k]*matrix[j][k] for k in range(3)), int(i==j), places=5)

    def test_spawn_and_required_hub_landmarks(self):
        spawns = self.xml.findall(".//Item[@class='SpawnLocation']")
        self.assertEqual(len(spawns), 1)
        self.assertEqual(spawns[0].find("Properties/bool[@name='Neutral']").text, 'true')
        names = {v.text for v in self.xml.findall(".//Properties/string[@name='Name']")}
        self.assertTrue({'ARMES', 'ARMURES', 'FRUITS', 'HarborFortifications', 'LighthouseTower', 'PortAvenue'} <= names)

    def test_walkable_land_and_dock_heights(self):
        tops = {}
        for p in self.parts:
            props = p.find('Properties')
            name = props.find("string[@name='Name']").text
            if name in ('Foundation', 'Beach', 'Plateau', 'Pier'):
                size = props.find("Vector3[@name='size']")
                y = float(props.find("CoordinateFrame[@name='CFrame']/Y").text)
                height = float(size.find('Y' if name == 'Pier' else 'X').text)
                tops[name] = y + height/2
        self.assertEqual(tops, {'Foundation': 4, 'Beach': 6, 'Plateau': 8, 'Pier': 8})

    def test_build_plots_and_budget(self):
        names = [v.text for v in self.xml.findall(".//Properties/string[@name='Name']")]
        self.assertEqual(names.count('FutureBuildPlots'), 13)
        self.assertEqual(sum(n.startswith('Plot_') for n in names), 52)
        self.assertLess(len(self.parts), 1500)


if __name__ == '__main__':
    unittest.main()
