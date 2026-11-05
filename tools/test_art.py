"""Geometric acceptance checks for the original landmark scenery."""
from pathlib import Path
import math
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]


class ArtTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xml=ET.parse(ROOT/'assets/Archipelago.rbxmx')
        cls.items=cls.xml.findall('.//Item')

    @staticmethod
    def name(i):return i.find("Properties/string[@name='Name']").text

    def test_landmarks_and_flowers_are_real_geometry(self):
        names=[self.name(i) for i in self.items]
        self.assertTrue({'MonumentalGate','FloweringGardens','CascadeGarden','GateIvy'}<=set(names))
        self.assertEqual(names.count('ArtPetalSource'),3)
        self.assertGreaterEqual(names.count('BlossomLeaf'),250)
        self.assertGreaterEqual(names.count('FlowerPetal'),150)
        self.assertEqual(names.count('WaterfallRibbon'),6)
        self.assertEqual(names.count('ForgedChainLink'),256)

    def test_gate_arch_has_stone_above_a_clear_opening(self):
        prisms=[i for i in self.items if self.name(i) in ('ArchVoussoir','ArchSpandrel')]
        self.assertGreater(len(prisms),40)
        def contains(item,point):
            props=item.find('Properties')
            f=props.find("CoordinateFrame[@name='CFrame']")
            pos=[float(f.find(k).text) for k in ('X','Y','Z')]
            size=[float(v.text) for v in props.find("Vector3[@name='size']")]
            local=[sum(float(f.find(f'R{j}{i}').text)*(point[j]-pos[j]) for j in range(3)) for i in range(3)]
            return all(abs(local[i])<=size[i]/2+1e-4 for i in range(3)) and local[1]+size[1]/2<=(local[2]/size[2]+.5)*size[1]+1e-4
        for degrees in range(4,177,13):
            a=math.radians(degrees)
            for radius in (21.5,23,24):
                point=(math.cos(a)*radius,28+math.sin(a)*radius,195)
                self.assertTrue(any(contains(i,point) for i in prisms),f'Arch masonry gap at {point}')
        for y in (10,15,25,35,45,48):
            self.assertFalse(any(contains(i,(0,y,195)) for i in prisms),'Arch obstructs gate opening')
        for y in (50,55,60,65):
            self.assertTrue(any(contains(i,(0,y,195)) for i in prisms),'Unclosed bridge')

    def test_visual_leaves_and_water_never_block_players(self):
        visual={'BlossomLeaf','BlossomMass','FernFrond','FlowerPetal','FlowerCenter','WaterfallRibbon',
                'FallingWaterGlint','GardenWater','ForgedChainLink','IvyLeaf'}
        count=0
        for i in self.items:
            if self.name(i) not in visual:continue
            count+=1
            self.assertEqual(i.find("Properties/bool[@name='CanCollide']").text,'false')
            self.assertEqual(i.find("Properties/bool[@name='CanQuery']").text,'false')
        self.assertGreater(count,600)

    def test_effects_use_existing_roblox_assets_and_bounded_lights(self):
        self.assertEqual(len(self.xml.findall(".//Item[@class='Fire']")),2)
        self.assertEqual(len(self.xml.findall(".//Item[@class='PointLight']")),16)
        for i in self.items:
            if i.get('class') not in ('Part','WedgePart'):continue
            c=i.find("Properties/Color3[@name='Color']")
            self.assertTrue(all(0<=float(channel.text)<=1 for channel in c))


if __name__=='__main__':unittest.main()
