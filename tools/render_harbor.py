#!/usr/bin/env python3
"""Optional geometry preview using NumPy/Pillow; NOT a Roblox Studio screenshot.

Usage: python3 tools/render_harbor.py [overview|street|rear|facade]
The map generator and Roblox build do not depend on these optional packages.
"""
import math
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
MODE = sys.argv[1] if len(sys.argv) > 1 else "overview"
WIDTH, HEIGHT = 1680, 1200
tree = ET.parse(ROOT / "assets/Archipelago.rbxmx")
hub = next(i for i in tree.findall("./Item/Item") if i.find("Properties/string[@name='Name']").text == "grand_port")
triangles = []


def add_mesh(points, faces, frame, pos, tint):
    vertices = np.array(points, dtype=float) @ frame.T + pos
    for face in faces:
        for k in range(1, len(face)-1):
            tri = vertices[[face[0], face[k], face[k+1]]]
            normal = np.cross(tri[1]-tri[0], tri[2]-tri[0])
            length = np.linalg.norm(normal)
            if length < .00001:
                continue
            normal /= length
            triangles.append((tri, np.array(tint), normal))


for item in hub.findall(".//Item"):
    if item.get("class") not in ("Part", "WedgePart", "SpawnLocation"):
        continue
    p = item.find("Properties")
    alpha = p.find("float[@name='Transparency']")
    if alpha is not None and float(alpha.text) >= 1:
        continue
    c = p.find("Color3[@name='Color']")
    tint = [float(c.find(k).text) for k in ("R", "G", "B")]
    frame = p.find("CoordinateFrame[@name='CFrame']")
    pos = np.array([float(frame.find(k).text) for k in ("X", "Y", "Z")])
    matrix = np.array([[float(frame.find(f"R{i}{j}").text) for j in range(3)] for i in range(3)])
    s = p.find("Vector3[@name='size']")
    sx, sy, sz = [float(s.find(k).text)/2 for k in ("X", "Y", "Z")]
    shape = p.find("token[@name='shape']")
    kind = shape.text if shape is not None else "1"
    if item.get("class") == "WedgePart":
        pts = [(-sx,-sy,-sz), (sx,-sy,-sz), (-sx,-sy,sz), (sx,-sy,sz), (-sx,sy,sz), (sx,sy,sz)]
        faces = [(0,2,3,1), (2,4,5,3), (0,1,5,4), (0,4,2), (1,3,5)]
    elif kind == "2":
        n = 20
        pts = [(side*sx, math.cos(k*math.tau/n)*sy, math.sin(k*math.tau/n)*sz) for side in (-1,1) for k in range(n)]
        faces = [tuple(reversed(range(n))), tuple(range(n,2*n))]
        faces += [(k, (k+1)%n, (k+1)%n+n, k+n) for k in range(n)]
    elif kind == "0":
        n, rings = 12, 8
        pts = [(math.cos(j*math.pi/rings)*sx,
                math.sin(j*math.pi/rings)*math.cos(k*math.tau/n)*sy,
                math.sin(j*math.pi/rings)*math.sin(k*math.tau/n)*sz)
               for j in range(rings+1) for k in range(n)]
        faces = [(j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k) for j in range(rings) for k in range(n)]
    else:
        pts = [(x*sx,y*sy,z*sz) for x,y,z in ((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))]
        faces = [(0,3,2,1),(4,5,6,7),(0,4,7,3),(1,2,6,5),(3,7,6,2),(0,1,5,4)]
    add_mesh(pts, faces, matrix, pos, tint)


# Match the native ocean's surface at Y=0 so submerged foundations are hidden.
add_mesh([(-3072,0,-3072),(-3072,0,3072),(3072,0,3072),(3072,0,-3072)],
         [(0,1,2,3)], np.eye(3), np.zeros(3), (63/255,103/255,117/255))

eye, target, scale = ((420,360,600), (0,8,30), 2.65) if MODE == "overview" else ((120,91,245),(0,18,-35),5.0)
if MODE == "rear":
    eye, target, scale = (-380,260,-530), (0,15,-25), 2.8
if MODE == "facade":
    eye, target, scale = (-12,29,4), (-56,18,-45), 26
eye, target = np.array(eye,dtype=float), np.array(target,dtype=float)
forward = (target-eye)/np.linalg.norm(target-eye)
near_depth = -np.linalg.norm(target-eye)+0.1
right = np.cross(forward, [0,1,0]); right /= np.linalg.norm(right)
up = np.cross(right,forward)
light = np.array([-.45, .85, .35]); light /= np.linalg.norm(light)
buffer = np.empty((HEIGHT, WIDTH, 3)); buffer[:] = (40,75,86)
depth = np.full((HEIGHT, WIDTH), np.inf)


def raster(tri, tint, normal):
    rel = tri-target
    coords = np.column_stack((rel@right*scale+WIDTH/2, -rel@up*scale+HEIGHT/2, rel@forward))
    if coords[:,2].max() < near_depth:
        return
    x0 = max(0,int(math.floor(coords[:,0].min())))
    x1 = min(WIDTH-1,int(math.ceil(coords[:,0].max())))
    y0 = max(0,int(math.floor(coords[:,1].min())))
    y1 = min(HEIGHT-1,int(math.ceil(coords[:,1].max())))
    if x1<x0 or y1<y0: return
    a,b,c = coords
    area=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
    if abs(area)<.0001: return
    yy,xx = np.mgrid[y0:y1+1,x0:x1+1]
    u=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/area
    v=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/area
    w=1-u-v
    z=u*a[2]+v*b[2]+w*c[2]
    region=depth[y0:y1+1,x0:x1+1]
    mask=(u>=0)&(v>=0)&(w>=0)&(z<region)
    if not mask.any(): return
    # Two-sided diffuse preview; actual Studio lighting/materials differ.
    diffuse=abs(normal@light)
    shaded=np.clip(tint*(.60+.40*diffuse)*255,0,255)
    buffer[y0:y1+1,x0:x1+1][mask]=shaded
    region[mask]=z[mask]


for tri, tint, normal in triangles:
    raster(tri,tint,normal)
image=Image.fromarray(buffer.astype(np.uint8))
draw=ImageDraw.Draw(image)
try:
    titlefont=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',30)
    smallfont=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
except OSError:
    titlefont=smallfont=ImageFont.load_default()
draw.rectangle((0,0,WIDTH,78), fill=(17,29,36))
draw.text((32,20), 'OP EMPIRE WARS  /  GRAND PORT  /  v0.4',fill=(236,224,194),font=titlefont)
draw.rectangle((0,HEIGHT-52,WIDTH,HEIGHT),fill=(17,29,36))
draw.text((32,HEIGHT-36),'Verification de geometrie hors Studio - ne montre pas le ciel, le brouillard ni les textures du jeu.',fill=(180,194,199),font=smallfont)
(ROOT/'build').mkdir(exist_ok=True)
dest=ROOT/'build'/f'Grand-Port-v0.4-{MODE}.png'
image.save(dest)
print(f'Rendered {len(triangles)} triangles: {dest}')
