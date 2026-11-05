"""Hand-authored harbor detailing; no external assets or runtime dependencies."""
import math
import random
import xml.etree.ElementTree as ET
from roofing import pitched_roof
from layout import rectangle_union


def decorate_hub(hub, *, obj, part, disc, prop, color, vec):
    rng = random.Random(20261105)
    wood = (83, 66, 52)
    iron = (49, 59, 65)
    stone = (122, 126, 124)
    brass = (165, 133, 74)
    warm = (249, 205, 135)
    detail = obj(hub, "Model", "HarborDetails")

    def name(item):
        return item.find("Properties/string[@name='Name']").text

    def group(title, parent=detail):
        return obj(parent, "Model", title)

    def p(parent, title, pos, size, tint=wood, mat="wood", rot=(0, 0, 0), solid=False, shape=1):
        item = part(parent, title, pos, size, tint, mat, rot, shape, collide=solid)
        if not solid:
            prop(item, "bool", "CanQuery", False)
        if min(size) < .35 or max(size) < 3:
            prop(item, "bool", "CastShadow", False)
        return item

    def beam(parent, title, a, b, width=.35, tint=wood, mat="wood", solid=False):
        dx, dy, dz = (b[i]-a[i] for i in range(3))
        length = math.sqrt(dx*dx+dy*dy+dz*dz)
        # Cylinder's X axis is aligned with the endpoint vector.
        yaw = -math.degrees(math.asin(dz/length))
        roll = math.degrees(math.atan2(dy, dx))
        return p(parent, title, tuple((a[i]+b[i])/2 for i in range(3)),
                 (length, width, width), tint, mat, (0, yaw, roll), solid, 2)

    def sign(parent, title, x, y, z, w=18, h=3.5, tint=wood):
        board = p(parent, "CarvedSign", (x, y, z), (w, h, .6), tint)
        for offset in (-h/2, h/2):
            p(parent, "SignBorder", (x, y+offset, z+.35), (w+.4, .25, .3), brass, "metal")
        gui = obj(board, "SurfaceGui", "Lettering")
        prop(gui, "token", "Face", 2)  # South / +Z: the storefront face.
        prop(gui, "float", "PixelsPerStud", 36)
        prop(gui, "token", "SizingMode", 1)
        text = obj(gui, "TextLabel", "Text")
        size = prop(text, "UDim2", "Size")
        for key, val in (("XS", 1), ("XO", 0), ("YS", 1), ("YO", 0)):
            ET.SubElement(size, key).text = str(val)
        prop(text, "float", "BackgroundTransparency", 1)
        prop(text, "string", "Text", title)
        prop(text, "bool", "TextScaled", True)
        prop(text, "bool", "TextWrapped", True)
        prop(text, "token", "Font", 4)
        color(text, "TextColor3", (238, 222, 186))
        return board

    def lantern(parent, x, y, z, light=False):
        p(parent, "LanternFoot", (x, y-1.35, z), (1.7, .35, 1.7), iron, "metal")
        p(parent, "LanternCap", (x, y+1.35, z), (2, .45, 2), iron, "metal")
        glow = p(parent, "LanternGlow", (x, y, z), (1.1, 2.1, 1.1), warm, "neon")
        for dx in (-.7, .7):
            for dz in (-.7, .7):
                p(parent, "LanternFrame", (x+dx, y, z+dz), (.15, 2.6, .15), iron, "metal")
        if light:
            lamp = obj(glow, "PointLight", "WarmPool")
            prop(lamp, "float", "Range", 22)
            prop(lamp, "float", "Brightness", .9)
            prop(lamp, "bool", "Shadows", False)
            color(lamp, "Color", warm)

    def barrel(parent, x, y, z, scale=1):
        r, h = 1.7*scale, 4*scale
        disc(parent, "CooperedBarrel", x, y+h/2, z, r, h, wood, "wood")
        for dy in (.65, h-.65):
            disc(parent, "BarrelHoop", x, y+dy, z, r+.09, .24, iron, "metal")
        disc(parent, "BarrelLid", x, y+h+.03, z, r-.1, .16, (107, 86, 62), "wood")
        for dx in (-.6, .6):
            p(parent, "LidSeam", (x+dx*scale, y+h+.12, z), (.07, .05, r*1.6), iron)

    def crate(parent, x, y, z, size=4):
        p(parent, "CargoCrate", (x, y+size/2, z), (size, size, size), (104, 86, 62), solid=True)
        for dx in (-size/2+.25, size/2-.25):
            p(parent, "CrateStrap", (x+dx, y+size/2, z+size/2+.08), (.45, size, .25), wood)
        for dy in (.25, size-.25):
            p(parent, "CrateRim", (x, y+dy, z+size/2+.1), (size, .45, .3), wood)
        length = size*1.22
        p(parent, "CrateDiagonal", (x, y+size/2, z+size/2+.3), (.4, length, .25), wood, rot=(0, 0, -40))

    def window(parent, x, y, z, w=6, h=7, face=1):
        p(parent, "WindowRecess", (x, y, z), (w+.8, h+.8, .4), iron, "metal")
        pane = p(parent, "AmberWindow", (x, y, z+face*.25), (w, h, .25), (166, 153, 119), "glass")
        prop(pane, "float", "Transparency", .15)
        for dx in (-w/2, 0, w/2):
            p(parent, "WindowMullion", (x+dx, y, z+face*.5), (.25, h+.5, .4), wood)
        for dy in (-h/2, 0, h/2):
            p(parent, "WindowCrossbar", (x, y+dy, z+face*.5), (w+.5, .3, .4), wood)
        p(parent, "StoneWindowSill", (x, y-h/2-.5, z+face*.4), (w+1.8, .8, 1.7), stone, "stone")
        for side in (-1, 1):
            p(parent, "Shutter", (x+side*(w/2+1.15), y, z+face*.4), (1.6, h, .5), (69, 82, 81))
            for dy in (-h/3, h/3):
                p(parent, "ShutterHinge", (x+side*(w/2+1.15), y+dy, z+face*.72), (1.7, .2, .2), iron, "metal")

    def flag(parent, x, y, z, tint, w=5, h=8):
        beam(parent, "BannerPole", (x, y-h-2, z), (x, y+1, z), .25, iron, "metal")
        p(parent, "HangingBanner", (x+w/2, y-h/2, z), (w, h, .15), tint, "fabric")
        p(parent, "BannerEmblem", (x+w/2, y-h*.45, z+.1), (w*.38, h*.33, .1), (211, 199, 168), "fabric", (0, 0, 45))

    # Replace hub floating labels with physical, framed signs, except the map board.
    for child in list(hub.findall("Item")):
        if name(child) == "SignAnchor":
            hub.remove(child)
    for child in hub.findall("Item"):
        if name(child) in ("PortAvenue", "ShopStreet", "ShopAccess"):
            props = child.find("Properties")
            props.find("token[@name='Material']").text = "880"
            col = props.find("Color3[@name='Color']")
            for v, tint in zip(col, (.40, .43, .43)):
                v.text = str(tint)

    buildings = [(-75, -60, 38, 30, 23, "ARMES"), (0, -60, 38, 30, 23, "ARMURES"),
                 (75, -60, 38, 30, 23, "FRUITS"), (-130, 55, 48, 36, 23, "GUILDE DES PIRATES"),
                 (130, 55, 48, 36, 23, "QUARTIER MARINE"), (-112, 150, 50, 40, 23, "CHANTIER NAVAL"),
                 (-92, -135, 44, 28, 23, "MARCHÉ"), (92, -135, 44, 28, 23, "MISSIONS / TUTORIEL")]
    for x, z, w, d, h, title in buildings:
        building = next(i for i in hub.findall("Item") if name(i) == title)
        for child in list(building.findall("Item")):
            if name(child) in ("RoofAssembly", "SignAnchor"):
                building.remove(child)
        model = group("Architecture", building)
        accent = (65, 80, 95) if "MARINE" in title else (84, 66, 59)
        y = 8
        pitched_roof(model, x=x, z=z, width=w, depth=d, wall_top=y+h, accent=accent,
                     detailed=True, obj=obj, part=part, prop=prop)
        # Foundations, half-timbering and corner quoins; the entry remains open.
        for side in (-1, 1):
            p(model, "StonePlinth", (x+side*w/2, 10, z), (2.8, 4, d+1.2), stone, "stone")
            p(model, "FrontPlinth", (x+side*(w/4+3), 10, z+d/2+.25), (w/2-6, 4, 2), stone, "stone")
            for dz in (-d/2, d/2):
                p(model, "CornerTimber", (x+side*(w/2-.6), y+h/2, z+dz), (1.1, h, 1.1), wood)
            for band in (16, 26):
                p(model, "SideBelt", (x+side*(w/2+.3), band, z), (.8, .8, d), wood)
            for dz in (-d/4, d/4):
                xx = x+side*(w/2+1.1)
                p(model, "SideWindowRecess", (xx, 20, z+dz), (.4, 7.5, 6.5), iron, "metal")
                pane = p(model, "SideWindowGlass", (xx+side*.3, 20, z+dz), (.2, 6.5, 5.5), (161, 153, 125), "glass")
                prop(pane, "float", "Transparency", .15)
                for zz in (-3, 0, 3):
                    p(model, "SideWindowFrame", (xx+side*.5, 20, z+dz+zz), (.4, 7.2, .3), wood)
                for yy in (-3.5, 0, 3.5):
                    p(model, "SideWindowFrame", (xx+side*.5, 20+yy, z+dz), (.4, .3, 6.5), wood)
            for k in range(5):
                p(model, "CornerQuoin", (x+side*(w/2+.35), 10+k*4, z+d/2+.3), (3, 1.6, 2.8), (135-k*3, 136-k*3, 130-k*3), "stone")
            p(model, "RainGutter", (x+side*(w/2+3.5), 30.6, z), (.7, .7, d+6), iron, "metal")
            beam(model, "Drainpipe", (x+side*(w/2+2), 9, z-d/2+2), (x+side*(w/2+2), 30, z-d/2+2), .6, iron, "metal")
            window(model, x+side*(w/4+3), 20, z+d/2+1.1, min(6, w/2-11), 7)
            window(model, x+side*w/4, 20, z-d/2-1.2, 6, 7, face=-1)
            # Entry jambs and lintel frame a twelve-stud wide, nineteen-stud high opening.
            p(model, "DoorJamb", (x+side*6.6, 17, z+d/2+1.4), (1.2, 18, 1.8), stone, "stone")
        p(model, "DoorLintel", (x, 27, z+d/2+1.3), (14.4, 2, 2), stone, "stone")
        p(model, "EntryThreshold", (x, 8.8, z+d/2+2), (12, 1.2, 4), stone, "stone", solid=True)
        p(model, "RearPlinth", (x, 10, z-d/2-.35), (w, 4, 2.7), stone, "stone")
        sign(model, title, x, 30, z+d/2+4, w-6, 3.8)
        lantern(model, x-9, 20, z+d/2+3, light=title in ("ARMES", "FRUITS", "QUARTIER MARINE"))
        p(model, "Chimney", (x-w/3, 37, z-d/4), (4, 13, 4), (95, 91, 85), "brick")
        p(model, "ChimneyCrown", (x-w/3, 43.7, z-d/4), (5, 1, 5), iron, "stone")
        # Interior: shelves, brackets, tiled counter fascia and back-wall inventory.
        for shelf in (14, 20):
            p(model, "WallShelf", (x, shelf, z-d/2+3), (w-8, .7, 4), wood)
            for dx in (-w/3, w/3):
                beam(model, "ShelfBracket", (x+dx, shelf-3, z-d/2+1), (x+dx, shelf, z-d/2+4), .35, iron, "metal")
        for dx in range(-int(w/2)+5, int(w/2)-3, 5):
            p(model, "CounterPanel", (x+dx, 11, z-1.8), (4.5, 5, .4), (106, 84, 59))
        p(model, "Countertop", (x, 14.3, z-4), (w-7, .8, 5), (121, 101, 74))
        barrel(model, x+w/2+4, 8, z+d/2-3)

    interiors = group("ShopDisplays")
    for dx in (-10, -5, 0, 5, 10):
        p(interiors, "SwordBlade", (-75+dx, 18, -71), (.65, 8, .35), (161, 173, 175), "metal", (0, 0, -12))
        p(interiors, "SwordGuard", (-75+dx-.9, 14.3, -71), (3.3, .5, .6), brass, "metal")
        p(interiors, "SwordGrip", (-75+dx-1.15, 12.8, -71), (.7, 2.6, .7), wood)
    for dx in (-10, 10):
        p(interiors, "ArmorStand", (dx, 14, -69), (1, 11, 1), wood)
        p(interiors, "Breastplate", (dx, 17, -68), (5, 5.7, 2.4), (95, 111, 120), "metal")
        p(interiors, "ArmorTrim", (dx, 19.7, -66.6), (5.2, .4, .3), brass, "metal")
        p(interiors, "Helmet", (dx, 22.4, -68.5), (3.3, 3.5, 3.3), (126, 141, 145), "metal", shape=0)
        for side in (-1, 1):
            p(interiors, "Pauldron", (dx+side*3.2, 18.6, -68), (2.1, 2, 3), iron, "metal", (0, 0, side*20))
    for dx, tint in ((-9, (173, 73, 60)), (0, (116, 94, 152)), (9, (192, 158, 65))):
        disc(interiors, "FruitBasket", 75+dx, 14.9, -64, 3.2, 1, wood, "wood")
        for k in range(4):
            a = k*math.pi/2
            fx, fz = 75+dx+math.cos(a)*1.5, -64+math.sin(a)*1.5
            p(interiors, "DisplayFruit", (fx, 16.2, fz), (2.1, 2.4, 2.1), tint, "plastic", shape=0)
            beam(interiors, "FruitStem", (fx, 17.1, fz), (fx+.35, 18, fz), .2, (65, 87, 51))

    streets = group("PavedStreets")
    paths = (("PirateWalk", -75, 98, 130, 10), ("MarineWalk", 75, 98, 130, 10),
                             ("PirateEntry", -130, 86, 12, 26), ("MarineEntry", 130, 86, 12, 26),
                             ("MarketLane", -39, -94, 10, 138), ("MissionLane", 39, -94, 10, 138),
                             ("RearSquare", 0, -128, 90, 45), ("RearLane", 0, -109, 200, 10),
                             ("MarketEntry", -92, -115, 12, 16), ("MissionEntry", 92, -115, 12, 16),
                             ("ShipyardWalk", -56, 179, 112, 10), ("ShipyardEntry", -112, 174, 12, 16))
    # Tessellate the union once: intersections no longer stack coplanar road faces.
    for x0, z0, x1, z1 in rectangle_union([(x-w/2, z-d/2, x+w/2, z+d/2) for _, x, z, w, d in paths]):
        part(streets, "UnifiedWalkway", ((x0+x1)/2, 8.16, (z0+z1)/2), (x1-x0, .3, z1-z0), (99, 105, 105), "stone")
    # Large paving slabs add rhythm, leaving the main spawn-to-quay axis unobstructed.
    for j in range(23):
        for side in (-1, 1):
            tint = (111+j%3*4, 115+j%3*4, 112+j%3*4)
            p(streets, "AvenuePaver", (side*5, 8.43, 45+j*8), (9.6, .12, 7.6), tint, "stone")
    for x in (-11, 11):
        for z in range(44, 229, 10):
            p(streets, "Kerb", (x, 8.5, z), (1.2, .7, 9.6), stone, "stone")
    for x in range(-90, 91, 10):
        for z in (-31, -23):
            p(streets, "MarketPaver", (x, 8.42, z), (9.5, .1, 7.5), stone, "stone")
    for angle in range(0, 360, 30):
        a = math.radians(angle)
        p(streets, "PlazaBorder", (40*math.cos(a), 8.5, 40*math.sin(a)), (10, .4, 2), (142, 141, 129), "stone", (0, -angle-90, 0))
    for angle in (0, 90, 180, 270):
        a = math.radians(angle)
        p(streets, "CompassInlay", (16*math.sin(a), 8.65, 16*math.cos(a)), (2.4, .12, 13), brass, "metal", (0, angle, 0))
    # Hide the bright spawn tile, retaining the original SpawnLocation and position.
    spawn = next(i for i in hub.findall("Item") if name(i) == "CentralSpawn")
    prop(spawn, "float", "Transparency", 1)

    square = group("CivicSquare")
    # Fountain is north of the shop block, not on the player's spawn.
    disc(square, "FountainFoot", 0, 8.6, -129, 15, 1.2, stone, "stone")
    for k in range(12):
        a = k*math.tau/12
        p(square, "BasinRim", (13*math.sin(a), 10, -129+13*math.cos(a)), (7, 2.5, 2), stone, "stone", (0, k*30, 0), solid=True)
    disc(square, "StillFountainWater", 0, 9.8, -129, 11.5, .2, (75, 111, 118), "glass")
    disc(square, "FountainPedestal", 0, 13, -129, 2.5, 8, stone, "stone")
    disc(square, "FountainUpperBowl", 0, 17.2, -129, 5.5, 1, stone, "stone")
    for x, z in ((-24, -112), (24, -112), (-24, -150), (24, -150), (-48, 17), (48, 17)):
        p(square, "BenchSeat", (x, 11, z), (12, 1, 3.3), wood, solid=True)
        p(square, "BenchBack", (x, 13, z-1.6), (12, 3.5, .7), wood)
        for dx in (-4.4, 4.4):
            p(square, "BenchLeg", (x+dx, 9.5, z), (.8, 3, 3), iron, "metal")
    for x in (-21, 21):
        for z in (55, 115, 166):
            p(square, "StreetlightBase", (x, 8.8, z), (3, 1.5, 3), stone, "stone")
            beam(square, "StreetlightPole", (x, 9, z), (x, 23, z), .6, iron, "metal")
            beam(square, "StreetlightArm", (x, 23, z), (x+2, 23, z), .45, iron, "metal")
            lantern(square, x+2, 21, z, light=True)
    sign(square, "GRAND PORT", 0, 26, 191, 35, 5)
    for side in (-1, 1):
        beam(square, "GateSignChain", (side*15, 29, 191), (side*15, 32, 191), .22, iron, "metal")

    market = group("MarketStalls")
    for sx in (-155, -115):
        sz = -92
        for dx in (-7.5, 7.5):
            for dz in (-4, 4):
                p(market, "StallPost", (sx+dx, 14, sz+dz), (.7, 12, .7), wood)
        p(market, "StallCounter", (sx, 11.5, sz+1), (16, 1.2, 7), wood, solid=True)
        for k in range(6):
            tint = (150, 137, 103) if k%2 else (75, 92, 87)
            p(market, "StripedCanvas", (sx-6.5+k*2.6, 19, sz+1), (2.65, .4, 12), tint, "fabric", (7, 0, 0))
            p(market, "AwningValance", (sx-6.5+k*2.6, 17.7, sz+7), (2.65, 1.8, .3), tint, "fabric")
        for k in range(5):
            p(market, "MarketProduce", (sx-5+k*2.5, 12.8, sz+1), (1.8, 1.6, 1.8), (147+k*10, 111+k*4, 61), "plastic", shape=0)
        crate(market, sx+11, 8, sz-2)
    for x, z in ((-151, -130), (-62, -150), (113, 79), (-152, 78)):
        barrel(market, x, 8, z)
        crate(market, x+5, 8, z+1, 3.5)

    quay = group("WorkingQuays")
    # Individual planks are visual skins over the original continuous collision decks.
    for j in range(27):
        p(quay, "PierPlank", (0, 8.06, 215+j*3.1), (17.7, .12, 2.9), (91+j%4*3, 73+j%4*3, 55+j%4*2))
    for j in range(25):
        p(quay, "CrossDockPlank", (-37+j*3.1, 8.08, 293), (2.9, .12, 15.7), (96+j%3*4, 77+j%3*3, 57))
    for dx in (-32, 32):
        for j in range(13):
            p(quay, "FingerPierPlank", (dx, 8.06, 295+j*3.1), (9.7, .12, 2.9), (97, 78+j%3*3, 58))
    for z in (230, 251, 272):
        for side in (-1, 1):
            p(quay, "QuayPost", (side*8.5, 10, z), (1.2, 7, 1.2), wood, solid=True)
            disc(quay, "PostIronCap", side*8.5, 13.6, z, .85, .35, iron, "metal")
            if z < 272:
                beam(quay, "SaggingMooringRope", (side*8.5, 12, z), (side*8.5, 10.7, z+10.5), .22, (139, 121, 85))
                beam(quay, "SaggingMooringRope", (side*8.5, 10.7, z+10.5), (side*8.5, 12, z+21), .22, (139, 121, 85))
    for x in (-28, 28):
        for z in (295, 327):
            disc(quay, "MooringBollard", x, 9, z, .9, 2, iron, "metal")
            p(quay, "BollardHead", (x, 10.2, z), (3.2, .5, 1), iron, "metal")
        lantern(quay, x, 15, 292, light=True)
        p(quay, "DockLampPost", (x, 11, 292), (.5, 6, .5), iron, "metal")
    for x, z in ((-19, 292), (-24, 288), (19, 296)):
        barrel(quay, x, 8.1, z, .8)
    # Vertical fenders sit outside the boarding lane and docking basin.
    for x in (-38, 38):
        for z in (306, 320):
            p(quay, "TimberFender", (x, 4, z), (2, 8, 2), (58, 53, 46))
    sign(quay, "EMBARCADÈRE 01", 0, 16, 279, 16, 2.8)
    for x in (-7, 7):
        p(quay, "PierSignPost", (x, 12, 279), (.5, 8, .5), wood)

    defenses = group("StoneworkAndDefenses")
    for side in (-1, 1):
        for course in range(4):
            for block in range(6):
                x = side*(47+block*12)
                p(defenses, "SeaWallAshlar", (x, 9.5+course*3.2, 200.3), (11.7, 2.9, .4),
                  (103+course*4+block%3*3, 111+course*3, 115+block%3*2), "stone")
        for dy in range(12, 37, 5):
            for dx in (-7, 7):
                p(defenses, "GateTowerQuoin", (side*31+dx, dy, 200.3), (4, 2.8, 1), stone, "stone")
        window(defenses, side*31, 28, 200.5, 3, 6)
        flag(defenses, side*40, 35, 201, (58, 75, 88), 4, 9)
        # Decorative coastal guns: stationary geometry, never a gameplay cannon.
        for cx in (side*68, side*96):
            p(defenses, "GunCarriage", (cx, 10, 207), (5, 3, 7), wood, solid=True)
            beam(defenses, "CoastalGunBarrel", (cx, 12, 204), (cx, 13, 213), 2.1, iron, "metal")
            for dx in (-3, 3):
                p(defenses, "CarriageWheel", (cx+dx, 9.5, 207), (.8, 3, 3), iron, "metal", shape=2)

    yard = group("ShipwrightYard")
    # Dry-docked hull with a keel, curved ribs and continuous overlapping strakes.
    bx, bz = -172, 110
    for dx in (-6, 6):
        p(yard, "HullTrestle", (bx+dx, 10, bz), (2, 4, 29), wood, solid=True)
    p(yard, "ShipKeel", (bx, 12, bz), (2, 2, 34), wood)
    for k in range(7):
        zz = bz-15+k*5
        width = 7.5*math.sin((k+1)*math.pi/8)
        for side in (-1, 1):
            beam(yard, "HullRib", (bx, 12, zz), (bx+side*width, 17, zz), .7, (128, 101, 68))
            beam(yard, "HullRib", (bx+side*width, 17, zz), (bx+side*(width+1), 22, zz), .7, wood)
            if k < 6:
                nextw = 7.5*math.sin((k+2)*math.pi/8)
                for height in (17, 19, 21):
                    beam(yard, "HullStrake", (bx+side*(width+.5), height, zz),
                         (bx+side*(nextw+.5), height, zz+5), .85, wood)
    p(yard, "CraneUpright", (-73, 22, 152), (2.4, 28, 2.4), wood, solid=True)
    beam(yard, "CraneBoom", (-73, 34, 152), (-56, 34, 152), 2, wood)
    beam(yard, "CraneBrace", (-73, 23, 152), (-58, 34, 152), 1.1, wood)
    beam(yard, "CraneCable", (-56, 34, 152), (-56, 18, 152), .22, iron, "metal")
    for k in range(5):
        p(yard, "LumberStack", (-91, 9+k*.65, 181), (22, .6, 2.7), (101+k*3, 84+k*2, 60))
    crate(yard, -143, 8, 160, 5)
    barrel(yard, -139, 8, 171)

    vegetation = group("CoastalGardens")
    # Planters cluster around facades, away from doorways and the quay avenue.
    for x, z in ((-99, -37), (-51, -37), (51, -37), (99, -37), (-160, 34), (160, 34), (-65, -164), (65, -164)):
        p(vegetation, "PlanterBox", (x, 9.4, z), (7, 2.8, 3), wood, solid=True)
        p(vegetation, "PlanterSoil", (x, 10.8, z), (6.4, .3, 2.5), (58, 54, 42), "ground")
        for k in range(5):
            p(vegetation, "PlanterShrub", (x-2.5+k*1.2, 11.5, z), (2, 2, 2), (65+k*4, 84+k*3, 61), "grass", shape=0)
    for x, z in ((-190, -70), (191, -72), (-155, -177), (155, -177), (-200, 65), (197, 65), (-70, -190), (70, -190)):
        height = rng.uniform(21, 28)
        beam(vegetation, "OakTrunk", (x, 8, z), (x+1, height, z), 2.2, wood, solid=True)
        for j in range(4):
            a = j*math.pi/2+.3
            tx, tz = x+math.cos(a)*5, z+math.sin(a)*5
            beam(vegetation, "OakBranch", (x, height-5, z), (tx, height+2, tz), .9, wood)
            p(vegetation, "OakCanopy", (tx, height+5, tz), (12, 10, 12), (57+j*4, 77+j*4, 57+j*2), "grass", shape=0)
    # North and side shoreline rock clusters, leaving the south port unobstructed.
    for k in range(31):
        a = math.radians(160+k*8)
        rr = 228+rng.uniform(-5, 8)
        x, z = math.sin(a)*rr, math.cos(a)*rr
        if abs(x) < 125 and z > 135:
            continue
        p(vegetation, "CoastalBoulder", (x, 5, z), (rng.uniform(5, 10), rng.uniform(5, 9), rng.uniform(5, 10)),
          (82+k%4*4, 90+k%4*4, 88+k%4*4), "rock", (k%3*8, k*37, 8), shape=0)
    for x, z in ((-178, -38), (178, -36), (-180, 95), (93, 172), (-63, 93), (64, 94), (-143, -191), (143, -190)):
        for j in range(6):
            p(vegetation, "CoastalGrass", (x+(j%3)*1.6, 9.3, z+(j//3)*1.8), (.25, 2.8+j%3, 1.5),
              (91, 105, 72), "grass", (0, j*37, 12-j*4))

    beacon = group("LighthouseDetails")
    for k in range(10):
        a = k*math.tau/10
        x, z = 150+math.sin(a)*12.5, 150+math.cos(a)*12.5
        p(beacon, "LanternGalleryPost", (x, 62, z), (.5, 9, .5), iron, "metal")
        nx, nz = 150+math.sin(a+math.tau/10)*12.5, 150+math.cos(a+math.tau/10)*12.5
        beam(beacon, "GalleryRail", (x, 61, z), (nx, 61, nz), .3, iron, "metal")
    for k in range(3):
        window(beacon, 150, 20+k*12, 160-k, 3, 5)
    disc(beacon, "LighthouseFoot", 150, 8.6, 150, 14, 1.2, stone, "stone")
    flag(beacon, -159, 32, 70, (66, 61, 58), 6, 9)
    flag(beacon, 159, 32, 70, (53, 76, 98), 6, 9)

    # Replace the placeholder map board with framed navigation artwork.
    navigation = group("NavigationBoard")
    board = next(i for i in hub.findall("Item") if name(i) == "MapBoard")
    hub.remove(board)
    p(navigation, "NavigationPanel", (38, 16, 110), (17, 12, 1), (54, 74, 81))
    for dx in (-9, 9):
        p(navigation, "BoardPost", (38+dx, 15, 110), (1.4, 14, 1.5), wood, solid=True)
    for dy in (-6.5, 6.5):
        p(navigation, "BoardFrame", (38, 16+dy, 110), (19, 1, 1.5), wood)
    for dx, dy in ((0, 0), (-4, 0), (4, 0), (0, -3), (0, 3), (-5, 3.8), (5, -3.8)):
        p(navigation, "MapIslandSilhouette", (38+dx, 16+dy, 110.7), (2, 1.2, .2), (171, 161, 110), "sand")
    sign(navigation, "ARCHIPEL · ROUTES MARITIMES", 38, 25, 110, 23, 2.8)

    landmarks = group("DistrictLandmarks")
    # Marine signal tower adjoining the HQ gives the eastern district a vertical silhouette.
    tx, tz = 164, 45
    p(landmarks, "MarineSignalTower", (tx, 34, tz), (17, 52, 19), (126, 132, 134), "stone", solid=True)
    for dy in (13, 32, 51, 60):
        p(landmarks, "TowerCornice", (tx, dy, tz), (19, 1.5, 21), stone, "stone")
    for dy in (23, 43):
        window(landmarks, tx, dy, tz+10, 4, 8)
    for dx in (-7, 0, 7):
        for dz in (-9, 9):
            p(landmarks, "SignalTowerMerlon", (tx+dx, 63, tz+dz), (4, 5, 3), stone, "stone")
    flag(landmarks, tx, 77, tz, (49, 76, 102), 7, 11)
    # Pirate guild: crossed spars and a maritime wheel rather than another copy of the HQ.
    beam(landmarks, "GuildMast", (-155, 8, 47), (-155, 53, 47), .8, wood, solid=True)
    beam(landmarks, "GuildYardarm", (-165, 46, 47), (-145, 46, 47), .6, wood)
    flag(landmarks, -155, 45, 47, (60, 57, 53), 9, 11)
    for k in range(8):
        a = k*math.tau/8
        na = (k+1)*math.tau/8
        beam(landmarks, "GuildWheelRim", (-130+4*math.sin(a), 35+4*math.cos(a), 74),
             (-130+4*math.sin(na), 35+4*math.cos(na), 74), .4, brass, "metal")
        beam(landmarks, "GuildWheelSpoke", (-130, 35, 74), (-130+5.5*math.sin(a), 35+5.5*math.cos(a), 74), .28, wood)
    # Distinct awnings add a readable color code while keeping clear headroom at each entry.
    for x, tint in ((-75, (112, 67, 54)), (0, (68, 85, 105)), (75, (102, 78, 115))):
        for strip in range(6):
            stripe = tint if strip%2 else (157, 148, 124)
            p(landmarks, "ShopAwning", (x-10+strip*4, 24.5, -40), (4.05, .3, 9), stripe, "fabric", (8, 0, 0))
            p(landmarks, "ShopValance", (x-10+strip*4, 23, -35.6), (4.05, 2, .3), stripe, "fabric")
        for dx in (-12, 12):
            beam(landmarks, "AwningBrace", (x+dx, 20, -44), (x+dx, 24.5, -35.5), .35, iron, "metal")
    # The weaponsmith's working anvil is tucked beside the shop, off the entrance.
    p(landmarks, "AnvilBlock", (-100, 10, -56), (4, 4, 4), wood, solid=True)
    p(landmarks, "AnvilBody", (-100, 13, -56), (5, 2, 3), iron, "metal")
    p(landmarks, "AnvilFace", (-100, 14.4, -56), (6.5, .8, 3), (128, 139, 145), "metal")
    beam(landmarks, "AnvilHorn", (-103, 14, -56), (-106, 14, -56), 1.3, iron, "metal")
    p(landmarks, "HammerHead", (-98, 15.1, -56), (1.5, 1, 1), iron, "metal")
    p(landmarks, "HammerHandle", (-98, 14.8, -54.3), (.35, .35, 3), wood)

    # Small cargo-handling crane on the quay, outside the central walking lane.
    p(quay, "CargoCraneBase", (-35, 9, 291), (6, 2, 6), stone, "stone")
    beam(quay, "CargoCraneMast", (-35, 10, 291), (-35, 29, 291), 1.2, wood)
    beam(quay, "CargoCraneJib", (-35, 29, 291), (-23, 29, 291), 1, wood)
    beam(quay, "CargoCraneBrace", (-35, 20, 291), (-25, 29, 291), .7, wood)
    beam(quay, "CargoRope", (-23, 29, 291), (-23, 16, 291), .15, (143, 122, 82))
    crate(quay, -23, 12, 291, 3.5)

    approaches = group("HarborApproachMarkers")
    for x, tint in ((-105, (181, 102, 70)), (105, (102, 158, 137))):
        marker = group("ChannelBuoy", approaches)
        disc(marker, "BuoyFloat", x, 1, 397, 3, 2, iron, "metal")
        disc(marker, "BuoyStripe", x, 2.2, 397, 2.7, .6, tint, "metal")
        beam(marker, "BuoyMast", (x, 2.5, 397), (x, 9, 397), .55, iron, "metal")
        lantern(marker, x, 10, 397)
        for j in range(16):
            a, b = j*math.tau/16, (j+1)*math.tau/16
            wash = beam(marker, "BuoyWaterline", (x+5*math.sin(a), .15, 397+5*math.cos(a)),
                        (x+5*math.sin(b), .15, 397+5*math.cos(b)), .13, (126, 158, 162), "glass")
            prop(wash, "float", "Transparency", .6)
    return detail
