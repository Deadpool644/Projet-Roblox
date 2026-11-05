#!/usr/bin/env python3
"""Generate the editable Roblox model, without external Python dependencies."""
import json
import math
import random
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "tools/world.json").read_text())
RNG = random.Random(644)
XML = ET.Element("roblox", version="4")
COUNT = 0
MATERIAL = {"grass": 1280, "sand": 1296, "rock": 896, "wood": 528,
            "stone": 880, "plastic": 272, "neon": 288, "metal": 1088}
PALETTE = {"grass": (79, 99, 75), "sand": (157, 151, 130),
           "rock": (77, 85, 94), "wood": (88, 71, 58),
           "stone": (112, 118, 121), "cream": (169, 166, 153), "metal": (62, 69, 77)}


def prop(item, tag, name, value=None):
    node = ET.SubElement(item.find("Properties"), tag, name=name)
    if value is not None:
        node.text = str(value).lower() if isinstance(value, bool) else str(value)
    return node


def obj(parent, cls, name):
    global COUNT
    COUNT += 1
    item = ET.SubElement(parent, "Item", {"class": cls, "referent": f"RBX{COUNT}"})
    ET.SubElement(item, "Properties")
    prop(item, "string", "Name", name)
    return item


def vec(item, tag, name, values):
    node = prop(item, tag, name)
    for key, value in zip(("X", "Y", "Z"), values):
        ET.SubElement(node, key).text = str(value)


def color(item, name, values):
    node = prop(item, "Color3", name)
    for key, value in zip(("R", "G", "B"), values):
        ET.SubElement(node, key).text = str(value / 255)


def part(parent, name, pos, size, tint="stone", material="stone", rotation=(0, 0, 0), shape=1, cls="Part", collide=True):
    item = obj(parent, cls, name)
    vec(item, "Vector3", "size", size)
    frame = prop(item, "CoordinateFrame", "CFrame")
    # Rz * Ry * Rx; cylinder's local X axis becomes vertical with Z=90 degrees.
    ax, ay, az = map(math.radians, rotation)
    cx, sx, cy, sy, cz, sz = math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay), math.cos(az), math.sin(az)
    matrix = (cz*cy, cz*sy*sx-sz*cx, cz*sy*cx+sz*sx,
              sz*cy, sz*sy*sx+cz*cx, sz*sy*cx-cz*sx,
              -sy, cy*sx, cy*cx)
    for key, value in zip(("X", "Y", "Z", "R00", "R01", "R02", "R10", "R11", "R12", "R20", "R21", "R22"), (*pos, *matrix)):
        ET.SubElement(frame, key).text = str(round(value, 6))
    color(item, "Color", PALETTE.get(tint, tint))
    prop(item, "token", "Material", MATERIAL[material])
    prop(item, "bool", "Anchored", True)
    prop(item, "bool", "CanCollide", collide)
    prop(item, "bool", "CanTouch", collide)
    prop(item, "token", "TopSurface", 0)
    prop(item, "token", "BottomSurface", 0)
    if cls == "Part":
        prop(item, "token", "shape", shape)
    return item


def disc(parent, name, x, y, z, radius, height, tint="grass", material="grass"):
    return part(parent, name, (x, y, z), (height, radius*2, radius*2), tint, material, (0, 0, 90), 2)


def value(parent, name, val):
    item = obj(parent, "StringValue", name)
    prop(item, "string", "Value", val)


def label(parent, text, pos, width=180):
    anchor = part(parent, "SignAnchor", pos, (1, 1, 1), "stone", collide=False)
    prop(anchor, "float", "Transparency", 1)
    gui = obj(anchor, "BillboardGui", "Sign")
    prop(gui, "bool", "AlwaysOnTop", False)
    prop(gui, "float", "MaxDistance", 240)
    size = prop(gui, "UDim2", "Size")
    for key, val in (("XS", 0), ("XO", width), ("YS", 0), ("YO", 48)):
        ET.SubElement(size, key).text = str(val)
    text_item = obj(gui, "TextLabel", "Title")
    size = prop(text_item, "UDim2", "Size")
    for key, val in (("XS", 1), ("XO", 0), ("YS", 1), ("YO", 0)):
        ET.SubElement(size, key).text = str(val)
    prop(text_item, "float", "BackgroundTransparency", 0.15)
    color(text_item, "BackgroundColor3", (24, 43, 55))
    color(text_item, "TextColor3", (255, 246, 214))
    prop(text_item, "string", "Text", text)
    prop(text_item, "bool", "TextScaled", True)
    prop(text_item, "bool", "TextWrapped", True)
    prop(text_item, "token", "Font", 4)


def building(parent, name, x, z, roof=(95, 69, 61), w=38, d=30, h=23, y=8):
    model = obj(parent, "Model", name)
    part(model, "Floor", (x, y+0.5, z), (w, 1, d), "wood", "wood")
    part(model, "Back", (x, y+h/2, z-d/2), (w, h, 2), "cream")
    for sign in (-1, 1):
        part(model, "Side", (x+sign*w/2, y+h/2, z), (2, h, d), "cream")
        # Wide entry, no invisible solid facade obstructing the shop.
        part(model, "Front", (x+sign*(w/4+3), y+h/2, z+d/2), (w/2-6, h, 2), "cream")
        part(model, "Roof", (x+sign*w/4, y+h+4, z), (w/2+5, 2, d+8), roof, "wood", (0, 0, -sign*22))
        part(model, "Post", (x+sign*(w/2-2), y+h/2, z+d/2+5), (2, h, 2), "wood", "wood")
    part(model, "Counter", (x, y+3, z-4), (w-8, 6, 4), "wood", "wood")
    label(model, name, (x, y+h+14, z))
    return model


def tree(parent, x, z, pine=False, base=8):
    h = RNG.randint(16, 25)
    part(parent, "Trunk", (x, base+h/2, z), (3, h, 3), "wood", "wood")
    if pine:
        for level in range(3):
            disc(parent, "PineCrown", x, base+h-6+level*5, z, 10-level*2.5, 7, (46, 73, 61))
    else:
        for angle in (0, 72, 144, 216, 288):
            a = math.radians(angle)
            part(parent, "PalmFrond", (x+6*math.sin(a), base+h, z+6*math.cos(a)),
                 (4, 1.2, 18), (55, 83, 61), "grass", (18, angle, 0), collide=False)


def dock(parent, x, z, r):
    model = obj(parent, "Model", "Harbor")
    part(model, "Pier", (x, 7.5, z+r+27), (18, 1, 86), "wood", "wood")
    part(model, "Landing", (x, 7.5, z+r+63), (78, 1, 16), "wood", "wood")
    for dx in (-32, 32):
        part(model, "Berth", (x+dx, 7.5, z+r+84), (10, 1, 42), "wood", "wood")
    for dz in (0, 28, 58):
        for dx in (-8, 8):
            part(model, "Pile", (x+dx, 2, z+r+dz), (2, 16, 2), "wood", "wood")
    # Broad, walkable stairs from deck (8) down to a low boarding platform (2).
    for n in range(6):
        part(model, "BoardingStep", (x+40+n*3, 7-n, z+r+63), (3, 2, 14), "wood", "wood")
    return model


WORLD = obj(XML, "Model", "Archipelago")
sea = part(WORLD, "OceanPreview", (0, -0.6, 0), (6144, 1, 6144), (39, 78, 91), "plastic", collide=False)
prop(sea, "float", "Transparency", 0.12)


def ground(cfg, tint="grass"):
    x, z, r = cfg["x"], cfg["z"], cfg["radius"]
    model = obj(WORLD, "Model", cfg["id"])
    value(model, "DisplayName", cfg["name"])
    value(model, "Difficulty", str(cfg.get("tier", 0)))
    value(model, "OwnershipBonusDesign", cfg.get("bonus", "Aucun — hub neutre"))
    # Overlapping lobes give each coast its own silhouette. Keep a wide central
    # plateau for building and the south landing, without copying reference islands.
    profile = {
        "forest": [(-.48, -.12, .65), (.15, -.48, .6), (.38, .14, .7)],
        "trade": [(-.5, -.25, .62), (.5, -.25, .62)],
        "quarry": [(-.45, -.45, .65), (.42, -.18, .7)],
        "coral": [(-.55, .12, .6), (.55, .12, .6), (0, -.5, .65)],
        "swamp": [(-.5, -.2, .7), (.4, -.4, .64), (.4, .35, .6)],
        "storm": [(-.55, -.25, .64), (.55, -.25, .64), (0, -.55, .6)],
        "ancient": [(-.4, -.4, .72), (.4, .4, .72)],
    }.get(cfg.get("theme"), [(-.35, -.4, .75), (.4, -.2, .7)])
    for dx, dz, scale in [(0, 0, 1 if cfg.get("tier", 0) == 0 else .87), *profile]:
        bx, bz, br = x+dx*r, z+dz*r, r*scale
        disc(model, "Foundation", bx, -10, bz, br+12, 28, "sand", "sand")
        # Beach top 6 then land top 8; 2-stud step is walkable.
        disc(model, "Beach", bx, 4, bz, br+16, 4, "sand", "sand")
        disc(model, "Plateau", bx, 6, bz, br, 4, tint)
    for k in range(9):
        a = k*math.tau/9
        disc(model, "Coast", x+math.cos(a)*(r-15), 2, z+math.sin(a)*(r-15), 32, 8, "sand", "sand")
    dock(model, x, z, r)
    return model


# Hub: clear spawn -> shops -> long main avenue -> central port.
hub = ground(CONFIG["hub"])
disc(hub, "SpawnPlaza", 0, 8.2, 0, 42, 0.4, "stone", "stone")
spawn = part(hub, "CentralSpawn", (0, 8.7, 0), (12, 1, 12), (87, 183, 193), cls="SpawnLocation")
prop(spawn, "bool", "Neutral", True)
prop(spawn, "float", "Duration", 0)
part(hub, "PortAvenue", (0, 8.2, 136), (20, 0.4, 192), "sand", "sand")
part(hub, "ShopStreet", (0, 8.2, -27), (190, 0.4, 16), "sand", "sand")
for x, title, tint in ((-75, "ARMES", (110, 64, 55)), (0, "ARMURES", (60, 77, 94)), (75, "FRUITS", (85, 64, 96))):
    building(hub, title, x, -60, tint)
    part(hub, "ShopAccess", (x, 8.2, -32), (12, 0.4, 20), "sand", "sand")
building(hub, "GUILDE DES PIRATES", -130, 55, (78, 84, 95), 48, 36)
building(hub, "QUARTIER MARINE", 130, 55, (60, 77, 94), 48, 36)
building(hub, "CHANTIER NAVAL", -112, 150, (59, 83, 80), 50, 40)
building(hub, "MARCHÉ", -92, -135, (112, 90, 62), 44, 28)
building(hub, "MISSIONS / TUTORIEL", 92, -135, (67, 83, 70), 44, 28)
fortifications = obj(hub, "Model", "HarborFortifications")
for side in (-1, 1):
    # A 40-stud opening keeps the main avenue to the pier clear.
    part(fortifications, "SeaWall", (side*67, 15, 195), (94, 14, 10), "stone")
    part(fortifications, "GateTower", (side*31, 23, 188), (20, 30, 24), "rock", "rock")
    for i in range(8):
        part(fortifications, "Merlon", (side*(25+i*12), 24, 195), (6, 4, 10), "stone")
    for dz in (-8, 8):
        part(fortifications, "TowerCrown", (side*31, 40, 188+dz), (22, 4, 5), "stone")
    part(fortifications, "LanternPost", (side*15, 14, 208), (1, 12, 1), "metal", "metal")
    lantern = part(fortifications, "Lantern", (side*15, 21, 208), (3, 4, 3), (255, 201, 122), "neon")
    light = obj(lantern, "PointLight", "WarmLight")
    prop(light, "float", "Range", 28)
    prop(light, "float", "Brightness", 1.5)
    color(light, "Color", (255, 201, 122))
label(hub, "GRAND PORT\nHub neutre · boutiques et départ", (0, 27, 27), 230)
label(hub, "PORT CENTRAL ↓", (0, 25, 165))
label(hub, "NAVIRE DE DÉPART\nEmplacement réservé", (0, 23, 298), 210)
label(hub, "TABLEAU DES ÎLES\nPremière escale : les Moissons", (38, 21, 110), 220)
part(hub, "MapBoard", (38, 14, 110), (16, 12, 2), "wood", "wood")
for y, radius, tint in ((17, 11, "cream"), (33, 10, (190, 77, 66)), (49, 9, "cream")):
    disc(hub, "LighthouseTower", 150, y, 150, radius, 16, tint, "stone")
disc(hub, "LighthouseLantern", 150, 60, 150, 12, 6, (255, 223, 131), "neon")
disc(hub, "LighthouseRoof", 150, 65, 150, 15, 3, (68, 91, 110), "metal")
for x, z in ((-185, -40), (185, -40), (-160, -115), (160, -115), (-160, 105), (85, 170), (-70, 85), (70, 85)):
    tree(hub, x, z)

for cfg in CONFIG["islands"]:
    x, z, r, theme = (cfg[k] for k in ("x", "z", "radius", "theme"))
    tint = {"volcano": (66, 66, 73), "storm": (98, 121, 132), "swamp": (88, 115, 93), "coral": (105, 180, 142)}.get(theme, "grass")
    island = ground(cfg, tint)
    tier = ("Débutant", "Intermédiaire", "Avancé")[cfg["tier"]-1]
    label(island, cfg["name"]+"\n"+tier, (x, 40, z+r-12), 220)
    part(island, "PortPath", (x, 8.2, z+r/2), (14, 0.4, r), "sand", "sand")
    pads = obj(island, "Model", "FutureBuildPlots")
    for i, (dx, dz) in enumerate(((-40, 20), (40, 20), (-40, -25), (40, -25))):
        part(pads, f"Plot_{i+1:02}", (x+dx, 8.15, z+dz), (28, 0.3, 28), (165, 178, 122), "sand")
    value(pads, "Status", "Emplacements visuels — construction non implémentée")
    # Decorations stay away from the dock approach and the reserved building plots.
    scenery = obj(island, "Model", "Scenery")
    for i in range(12 if theme == "forest" else 6):
        a = math.pi + i*math.pi/5
        tx, tz = x+math.cos(a)*(r-32), z+math.sin(a)*(r-32)
        if theme in ("forest", "farm", "trade", "coral", "wind"):
            tree(scenery, tx, tz, theme in ("forest", "farm"))
        else:
            part(scenery, "Cliff", (tx, 13, tz), (25, 18+i%3*6, 22), "rock", "rock", (0, i*27, 0))
    if theme in ("farm", "wind"):
        disc(scenery, "Windmill", x, 26, z-65, 10, 36, "cream", "stone")
        for angle in (35, 125):
            part(scenery, "WindmillSail", (x, 37, z-53), (3, 40, 1.5), "wood", "wood", (0, 0, angle), collide=False)
        if theme == "farm":
            for i in range(6):
                part(scenery, "CropRow", (x-70+i*9, 9, z-52), (3, 2, 30), (222, 186, 76), "grass")
    if theme in ("trade", "forest", "forge"):
        building(scenery, {"trade": "HALLE MARCHANDE", "forest": "SCIERIE", "forge": "FORGES"}[theme], x, z-75, (146, 84, 60))
    if theme == "forge":
        for dx in (-30, 30):
            part(scenery, "Chimney", (x+dx, 32, z-80), (12, 48, 12), "rock", "rock")
    if theme in ("fort", "citadel", "ancient"):
        for dx in (-65, 65):
            part(scenery, "Tower", (x+dx, 28, z-65), (23, 40, 23), "stone")
            for offset in (-8, 8):
                part(scenery, "Battlement", (x+dx+offset, 51, z-65), (5, 6, 23), "stone")
        part(scenery, "Rampart", (x, 24, z-74), (110, 32, 10), "stone")
        if theme == "ancient":
            for dx in (-24, 0, 24):
                disc(scenery, "TempleColumn", x+dx, 24, z-45, 5, 32, "cream", "stone")
    if theme == "volcano":
        for i in range(5):
            disc(scenery, "VolcanoSlope", x, 15+i*12, z-70, 80-i*12, 12, (64, 61, 68), "rock")
        disc(scenery, "Crater", x, 70, z-70, 24, 3, (255, 117, 36), "neon")
    if theme == "coral":
        for i in range(9):
            part(scenery, "ReefMarker", (x-r-24, 3, z-80+i*18), (7, 12, 7), (220, 124, 143), "rock")
    if theme == "swamp":
        disc(scenery, "MarshPool", x, 8.15, z-65, 28, 0.3, (62, 109, 112), "plastic")
    if theme in ("storm", "quarry"):
        for i in range(3):
            part(scenery, "HighRidge", (x-60+i*45, 22+i*8, z-70), (38, 28+i*16, 35), "rock", "rock", (0, i*25, 0))

(ROOT / "assets").mkdir(exist_ok=True)
ET.indent(XML)
ET.ElementTree(XML).write(ROOT / "assets/Archipelago.rbxmx", encoding="utf-8", xml_declaration=True)
parts = len(XML.findall(".//Item[@class='Part']")) + len(XML.findall(".//Item[@class='SpawnLocation']"))
print(f"Generated {len(CONFIG['islands'])+1} islands, {parts} anchored parts, {COUNT} instances")
