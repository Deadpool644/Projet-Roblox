"""Closed roofs derived from one pitch/eave profile, shared by every building."""
import math


def pitched_roof(parent, *, x, z, width, depth, wall_top, accent, detailed,
                 obj, part, prop):
    roof = obj(parent, "Model", "RoofAssembly")
    pitch = math.radians(26)
    overhang, thickness = 3, .8
    run = width/2+overhang
    ridge = wall_top+run*math.tan(pitch)
    # Public construction dimensions also allow independent geometry checks.
    wall_width = width+2  # Include the one-stud wall thickness outside each side.
    for key, val in (("Width", wall_width), ("Depth", depth), ("WallTop", wall_top),
                     ("RidgeHeight", ridge), ("CenterX", x), ("CenterZ", z)):
        v = obj(roof, "NumberValue", key)
        prop(v, "double", "Value", val)

    for side in (-1, 1):
        normal = (side*math.sin(pitch), math.cos(pitch))

        def surface(title, offset, span, normal_offset, thick, tint):
            return part(roof, title,
                        (x+side*offset+normal[0]*normal_offset,
                         wall_top+(run-offset)*math.tan(pitch)+normal[1]*normal_offset, z),
                        (span/math.cos(pitch), thick, depth+2*overhang), tint, "slate",
                        (0, 0, -side*26), collide=title == "RoofSlope")

        surface("RoofSlope", run/2, run, thickness/2, thickness, accent)
        if detailed:
            for course in range(5):
                tint = tuple(v+course*2 for v in accent)
                # Distinct courses have open seams, no coplanar overlapping tiles.
                surface("SlateCourse", (course+.5)*run/5, run/5-.10,
                        thickness+.12, .16, tint)
        part(roof, "EaveBeam", (x+side*run, wall_top-.3, z), (1, .9, depth+7),
             (83, 66, 52), "wood", collide=False)

    part(roof, "RoofRidge", (x, ridge+.65, z), (1.65, 1.3, depth+7), (54, 62, 68), "slate", collide=False)
    skirt = (overhang-1)*math.tan(pitch)
    triangle_height = wall_width/2*math.tan(pitch)
    for end, zz in (("Front", z+depth/2), ("Rear", z-depth/2)):
        end_model = obj(roof, "Model", end+"Gable")
        part(end_model, "GableSkirt", (x, wall_top+skirt/2, zz), (wall_width, skirt, 2),
             (169, 166, 153), "plaster")
        for side in (-1, 1):
            part(end_model, "GableTriangle",
                 (x+side*wall_width/4, wall_top+skirt+triangle_height/2, zz),
                 (2, triangle_height, wall_width/2), (169, 166, 153), "plaster",
                 (0, -90 if side == 1 else 90, 0), cls="WedgePart")
        part(end_model, "GableTie", (x, wall_top+.25, zz+(1.25 if end == "Front" else -1.25)),
             (width+1, .75, .5), (83, 66, 52), "wood", collide=False)
        part(end_model, "GableKingPost", (x, (wall_top+ridge)/2, zz+(1.25 if end == "Front" else -1.25)),
             (.65, ridge-wall_top, .5), (83, 66, 52), "wood", collide=False)
    return roof
