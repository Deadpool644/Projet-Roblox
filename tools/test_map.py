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
        # Includes the coast-following enclosure, six bastions and both stairs.
        self.assertLess(len(self.parts), 4500)

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

    def test_building_shells_have_structural_corners_without_overlaid_stones(self):
        names=[v.text for v in self.xml.findall(".//Properties/string[@name='Name']")]
        self.assertNotIn('CornerQuoin',names)
        self.assertNotIn('StonePlinth',names)
        buildings=[i for i in self.xml.findall(".//Item[@class='Model']")
                   if any(p.find("Properties/string[@name='Name']").text=='CornerPier' for p in i.findall('Item'))]
        self.assertEqual(len(buildings),11)
        for building in buildings:
            shell=[]
            corners=0
            for item in building.findall('Item'):
                props=item.find('Properties')
                name=props.find("string[@name='Name']").text
                if name not in ('CornerPier','WallBase','Back','Front','Side','EntryHeader'):
                    continue
                corners+=name=='CornerPier'
                frame=props.find("CoordinateFrame[@name='CFrame']")
                pos=[float(frame.find(k).text) for k in ('X','Y','Z')]
                size=[float(v.text) for v in props.find("Vector3[@name='size']")]
                shell.append([(v-s/2,v+s/2) for v,s in zip(pos,size)])
            self.assertEqual(corners,4)
            for i,a in enumerate(shell):
                for b in shell[i+1:]:
                    self.assertFalse(all(min(a[k][1],b[k][1])-max(a[k][0],b[k][0])>1e-6 for k in range(3)),
                                     'Wall and structural corner overlap')

    def test_fort_enclosure_volume_is_continuous(self):
        fort=next(i for i in self.xml.findall(".//Item[@class='Model']") if i.find("Properties/string[@name='Name']").text=='IslandFortress')
        path=next(i for i in fort.findall('Item') if i.find("Properties/string[@name='Name']").text=='PerimeterPath')
        nodes=[tuple(float(i.find(f"Properties/Vector3[@name='Value']/{k}").text) for k in ('X','Z')) for i in path.findall('Item')]
        self.assertEqual(nodes[0],(114,195))
        self.assertEqual(nodes[-1],(-114,195))
        self.assertGreater(max(z for x,z in nodes),190)
        self.assertLess(min(z for x,z in nodes),-230)
        self.assertLess(min(x for x,z in nodes),-230)
        self.assertGreater(max(x for x,z in nodes),230)
        volumes=[i for i in fort.findall('.//Item') if i.find("Properties/string[@name='Name']").text=='CurtainVolume']
        prisms=[p for volume in volumes for p in volume.findall("Item[@class='WedgePart']")]
        def contains(p,point):
            props=p.find('Properties')
            f=props.find("CoordinateFrame[@name='CFrame']")
            off=[point[i]-float(f.find(k).text) for i,k in enumerate(('X','Y','Z'))]
            local=[sum(float(f.find(f'R{j}{i}').text)*off[j] for j in range(3)) for i in range(3)]
            size=[float(v.text) for v in props.find("Vector3[@name='size']")]
            return all(abs(local[i])<=size[i]/2+1e-4 for i in range(3)) and local[1]+size[1]/2 <= (local[2]/size[2]+.5)*size[1]+1e-4
        for a,b in zip(nodes,nodes[1:]):
            dx,dz=b[0]-a[0],b[1]-a[1]
            length=math.hypot(dx,dz)
            for t in (.03,.2,.5,.8,.97):
                for offset in (-4.4,0,4.4):
                    point=(a[0]+dx*t-dz/length*offset,15,a[1]+dz*t+dx/length*offset)
                    self.assertTrue(any(contains(p,point) for p in prisms),f'Fort wall gap at {point}')
        bastions=[i for i in fort.findall('Item') if i.find("Properties/string[@name='Name']").text.startswith('Bastion_')]
        self.assertEqual(len(bastions),6)

    def test_fort_stair_treads_reach_wall_deck(self):
        stairs=[i for i in self.xml.findall(".//Item[@class='Model']") if i.find("Properties/string[@name='Name']").text in ('WestStair','EastStair')]
        self.assertEqual(len(stairs),2)
        for stair in stairs:
            steps=[]
            for item in stair.findall('Item'):
                props=item.find('Properties')
                if props.find("string[@name='Name']").text!='RampartTread': continue
                frame=props.find("CoordinateFrame[@name='CFrame']")
                size=[float(v.text) for v in props.find("Vector3[@name='size']")]
                self.assertGreaterEqual(size[2],5)
                steps.append(float(frame.find('Y').text)+size[1]/2)
            self.assertEqual(sorted(steps),list(range(9,23)))

    def test_fort_wall_top_faces_do_not_overlap(self):
        # Project the actual WedgePart top faces; a positive intersection would
        # reintroduce competing textures on the chemin de ronde.
        caps=[]
        for volume in self.xml.findall(".//Item[@class='Model']"):
            if volume.find("Properties/string[@name='Name']").text!='CurtainVolume': continue
            for p in volume.findall("Item[@class='WedgePart']"):
                props=p.find('Properties')
                f=props.find("CoordinateFrame[@name='CFrame']")
                pos=[float(f.find(k).text) for k in ('X','Y','Z')]
                half=[float(v.text)/2 for v in props.find("Vector3[@name='size']")]
                x=half[0]*(1 if float(f.find('R10').text)>0 else -1)
                tri=[]
                for local in ((x,-half[1],-half[2]),(x,-half[1],half[2]),(x,half[1],half[2])):
                    world=[pos[i]+sum(float(f.find(f'R{i}{j}').text)*local[j] for j in range(3)) for i in range(3)]
                    self.assertAlmostEqual(world[1],22,places=4)
                    tri.append((world[0],world[2]))
                def cross(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
                if cross(*tri)<0: tri.reverse()
                caps.append(tri)
        def clipped(subject,clip):
            for a,b in zip(clip,clip[1:]+clip[:1]):
                result=[]
                if not subject: break
                for prev,cur in zip(subject[-1:]+subject[:-1],subject):
                    dp,dc=cross(a,b,prev),cross(a,b,cur)
                    if (dp>=0)!=(dc>=0):
                        t=dp/(dp-dc)
                        result.append((prev[0]+(cur[0]-prev[0])*t,prev[1]+(cur[1]-prev[1])*t))
                    if dc>=0: result.append(cur)
                subject=result
            return subject
        self.assertGreater(len(caps),100)
        for index,a in enumerate(caps):
            for b in caps[index+1:]:
                polygon=clipped(a[:],b)
                area=abs(sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(polygon,polygon[1:]+polygon[:1])))/2
                self.assertLess(area,.01,'Overlapping wall-walk cap faces')

    def test_wall_walk_has_avatar_clearance(self):
        # True local-space containment, including the inclined prism faces.
        # AABBs alone would falsely classify the walk as inside its mitered rails.
        colliders=[]
        for item in self.parts:
            props=item.find('Properties')
            if props.find("bool[@name='CanCollide']").text!='true': continue
            f=props.find("CoordinateFrame[@name='CFrame']")
            pos=[float(f.find(k).text) for k in ('X','Y','Z')]
            size=[float(v.text) for v in props.find("Vector3[@name='size']")]
            matrix=[[float(f.find(f'R{i}{j}').text) for j in range(3)] for i in range(3)]
            ext=[sum(abs(matrix[i][j])*size[j]/2 for j in range(3)) for i in range(3)]
            if pos[1]+ext[1]<=22.1 or pos[1]-ext[1]>=28.3: continue
            shape=props.find("token[@name='shape']")
            kind='wedge' if item.get('class')=='WedgePart' else shape.text if shape is not None else '1'
            colliders.append((props.find("string[@name='Name']").text,pos,size,matrix,ext,kind))
        path=next(i for i in self.xml.findall(".//Item[@class='Folder']") if i.find("Properties/string[@name='Name']").text=='PerimeterPath')
        nodes=[tuple(float(i.find(f"Properties/Vector3[@name='Value']/{k}").text) for k in ('X','Z')) for i in path.findall('Item')]
        nodes=[(106.5,194),*nodes,(-106.5,194)]
        for a,b in zip(nodes,nodes[1:]):
            for t in (.04,.5,.96):
                x,z=a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t
                for angle in range(0,360,45):
                    px,pz=x+2*math.sin(math.radians(angle)),z+2*math.cos(math.radians(angle))
                    for y in (22.2,24.5,28):
                        for name,pos,size,matrix,ext,kind in colliders:
                            delta=[px-pos[0],y-pos[1],pz-pos[2]]
                            if any(abs(delta[i])>ext[i]+1e-5 for i in range(3)): continue
                            local=[sum(matrix[j][i]*delta[j] for j in range(3)) for i in range(3)]
                            inside=all(abs(local[i])<size[i]/2-1e-5 for i in range(3))
                            if kind=='wedge':
                                inside=inside and local[1]+size[1]/2 < (local[2]/size[2]+.5)*size[1]-1e-5
                            elif kind=='2':
                                inside=abs(local[0])<size[0]/2 and (local[1]/(size[1]/2))**2+(local[2]/(size[2]/2))**2<1-1e-5
                            elif kind=='0':
                                inside=sum((local[i]/(size[i]/2))**2 for i in range(3))<1-1e-5
                            self.assertFalse(inside,f'{name} blocks wall walk at {(px,y,pz)}')


if __name__ == '__main__':
    unittest.main()
