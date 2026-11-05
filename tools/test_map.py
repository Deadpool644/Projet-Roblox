"""Structural and layout checks. Roblox Studio playtests remain necessary."""
import collections
import json
import math
import hashlib
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class MapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = json.loads((ROOT / 'tools/world.json').read_text())
        cls.xml = ET.parse(ROOT / 'assets/Archipelago.rbxmx')
        cls.parts = [p for p in cls.xml.findall('.//Item') if p.get('class') in ('Part', 'SpawnLocation', 'WedgePart')]

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
        self.assertLess(len(self.parts), 4000)

    def test_original_island_bases_preserved(self):
        geometry = []
        for item in self.parts:
            props = item.find('Properties')
            name = props.find("string[@name='Name']").text
            if name in ('Foundation', 'Beach', 'Plateau', 'Coast'):
                geometry.append([name, [float(n.text) for n in props.find("CoordinateFrame[@name='CFrame']")],
                                 [float(n.text) for n in props.find("Vector3[@name='size']")]])
        digest = hashlib.sha256(json.dumps(geometry, sort_keys=True).encode()).hexdigest()
        baseline = json.loads((ROOT/'tools/coastline-baseline.json').read_text())
        self.assertEqual(digest, baseline['sha256'])

    def test_light_budget_and_details(self):
        self.assertLessEqual(len(self.xml.findall(".//Item[@class='PointLight']")), 16)
        names = {v.text for v in self.xml.findall(".//Properties/string[@name='Name']")}
        self.assertTrue({'MarineSignalTower', 'HullStrake', 'SwordBlade', 'Breastplate', 'DisplayFruit',
                         'NavigationPanel', 'PierPlank', 'SlateCourse', 'FountainFoot', 'WindowMullion'} <= names)

    def test_principal_routes_have_character_clearance(self):
        # A 4-stud-wide, 6-stud-high avatar envelope along hub footpaths.
        # This checks static obstacles, not actual Studio character physics.
        samples = [(0, z) for z in range(0, 292, 2)]
        for x in (-75, 0, 75):
            samples += [(x, z) for z in range(-42, -25, 2)]
        for side in (-1, 1):
            samples += [(side*x, 98) for x in range(0, 131, 2)]
            samples += [(side*130, z) for z in range(75, 99, 2)]
        obstacles = []
        for item in self.parts:
            props = item.find('Properties')
            if props.find("bool[@name='CanCollide']").text != 'true':
                continue
            frame = props.find("CoordinateFrame[@name='CFrame']")
            center = [float(frame.find(k).text) for k in ('X','Y','Z')]
            dims = [float(n.text) for n in props.find("Vector3[@name='size']")]
            extents = [sum(abs(float(frame.find(f'R{i}{j}').text))*dims[j]/2 for j in range(3)) for i in range(3)]
            # Floor and threshold surfaces can be up to 9.5 studs high.
            if center[1]+extents[1] <= 9.5 or center[1]-extents[1] >= 15.5:
                continue
            obstacles.append((props.find("string[@name='Name']").text, center, extents))
        for x, z in samples:
            for name, center, extents in obstacles:
                self.assertFalse(abs(x-center[0]) < extents[0]+2 and abs(z-center[2]) < extents[2]+2,
                                 f'{name} blocks route at {(x,z)}')

    def test_gables_close_both_ends_of_every_roof(self):
        roofs = [i for i in self.xml.findall(".//Item[@class='Model']")
                 if i.find("Properties/string[@name='Name']").text == 'RoofAssembly']
        self.assertEqual(len(roofs), 11)
        for roof in roofs:
            dims = {i.find("Properties/string[@name='Name']").text: float(i.find("Properties/double[@name='Value']").text)
                    for i in roof.findall("Item[@class='NumberValue']")}
            for end in ('Front', 'Rear'):
                gable = next(i for i in roof.findall('Item') if i.find("Properties/string[@name='Name']").text == end+'Gable')
                pieces = [i for i in gable.findall('Item') if i.get('class') in ('Part','WedgePart')]
                for fraction in (-.49, -.3, -.1, 0, .1, .3, .49):
                    dx = dims['Width']*fraction
                    top = dims['RidgeHeight']-abs(dx)*math.tan(math.radians(26))
                    for vertical in (.05,.3,.65,.95):
                        point = [dims['CenterX']+dx, dims['WallTop']+(top-dims['WallTop'])*vertical,
                                 dims['CenterZ']+(1 if end=='Front' else -1)*dims['Depth']/2]
                        covered = False
                        for piece in pieces:
                            props=piece.find('Properties')
                            frame=props.find("CoordinateFrame[@name='CFrame']")
                            offset=[point[i]-float(frame.find(k).text) for i,k in enumerate(('X','Y','Z'))]
                            local=[sum(float(frame.find(f'R{j}{i}').text)*offset[j] for j in range(3)) for i in range(3)]
                            size=[float(v.text) for v in props.find("Vector3[@name='size']")]
                            inside=all(abs(local[i])<=size[i]/2+1e-5 for i in range(3))
                            if piece.get('class')=='WedgePart':
                                inside=inside and local[1]+size[1]/2 <= (local[2]/size[2]+.5)*size[1]+1e-5
                            covered=covered or inside
                        self.assertTrue(covered, f'{end} gable hole at {point}')

    def test_gate_curtains_and_crenels_do_not_intersect_towers(self):
        def bounds(p):
            props=p.find('Properties')
            f=props.find("CoordinateFrame[@name='CFrame']")
            pos=[float(f.find(k).text) for k in ('X','Y','Z')]
            size=[float(v.text) for v in props.find("Vector3[@name='size']")]
            return [(v-s/2,v+s/2) for v,s in zip(pos,size)]
        masonry=[p for p in self.parts if p.find("Properties/string[@name='Name']").text in ('SeaWall','GateTower','Merlon')]
        for index,a in enumerate(masonry):
            for b in masonry[index+1:]:
                ba,bb=bounds(a),bounds(b)
                overlap=[min(ba[k][1],bb[k][1])-max(ba[k][0],bb[k][0]) for k in range(3)]
                self.assertFalse(all(v>1e-6 for v in overlap),'Intersecting gate masonry')
        curtains=[p for p in masonry if p.find("Properties/string[@name='Name']").text=='SeaWall']
        for p in self.parts:
            if p.find("Properties/string[@name='Name']").text=='SeaWallAshlar':
                self.assertGreater(bounds(p)[2][0],max(bounds(c)[2][1] for c in curtains))

    def test_paving_junctions_have_no_coplanar_overlaps(self):
        rects=[]
        for p in self.parts:
            props=p.find('Properties')
            if props.find("string[@name='Name']").text!='UnifiedWalkway':
                continue
            frame=props.find("CoordinateFrame[@name='CFrame']")
            x,z=float(frame.find('X').text),float(frame.find('Z').text)
            size=[float(v.text) for v in props.find("Vector3[@name='size']")]
            rects.append((x-size[0]/2,z-size[2]/2,x+size[0]/2,z+size[2]/2))
        self.assertGreater(len(rects),10)
        for i,a in enumerate(rects):
            for b in rects[i+1:]:
                self.assertFalse(min(a[2],b[2])-max(a[0],b[0])>1e-6 and min(a[3],b[3])-max(a[1],b[1])>1e-6)


if __name__ == '__main__':
    unittest.main()
