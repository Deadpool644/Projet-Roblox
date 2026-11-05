"""Coast-following fort with mitered, non-overlapping wall prisms.

Every wall section is a planar polygon extruded vertically. Right-triangle
prisms fit exactly, avoiding stacks of boxes with coincident top surfaces.
"""
import math
import xml.etree.ElementTree as ET


def build_fortress(hub, *, obj, part, disc, prop):
    stone = (111, 119, 122)
    cap = (134, 139, 137)
    fort = obj(hub, "Model", "IslandFortress")

    def number(parent, name, value):
        item = obj(parent, "NumberValue", name)
        prop(item, "double", "Value", value)

    number(fort, "WallThickness", 10)
    number(fort, "DeckHeight", 22)
    circles = []
    for item in hub.findall('Item'):
        if item.find("Properties/string[@name='Name']").text != 'Plateau':
            continue
        frame = item.find("Properties/CoordinateFrame[@name='CFrame']")
        size = item.find("Properties/Vector3[@name='size']")
        circles.append((float(frame.find('X').text), float(frame.find('Z').text), float(size.find('Y').text)/2))

    def coast(angle):
        dx, dz = math.sin(angle), math.cos(angle)
        radius = 0
        for x, z, r in circles:
            projection = x*dx+z*dz
            discriminant = r*r-x*x-z*z+projection*projection
            if discriminant >= 0:
                radius = max(radius, projection+math.sqrt(discriminant))
        return (radius+8)*dx, (radius+8)*dz

    nodes = [(114., 195.), (142., 195.)]
    nodes += [coast(math.radians(angle)) for angle in range(45, 316, 9)]
    nodes += [(-142., 195.), (-114., 195.)]
    path = obj(fort, "Folder", "PerimeterPath")
    for i, (x,z) in enumerate(nodes):
        item = obj(path, 'Vector3Value', f'Node_{i:02}')
        value = prop(item, 'Vector3', 'Value')
        for k,v in zip(('X','Y','Z'), (x,22,z)):
            ET.SubElement(value,k).text = str(v)

    def unit(a,b):
        dx,dz = b[0]-a[0], b[1]-a[1]
        length = math.hypot(dx,dz)
        return dx/length,dz/length

    tangents = [unit(a,b) for a,b in zip(nodes,nodes[1:])]
    miters=[]
    for i in range(len(nodes)):
        prev=tangents[max(0,i-1)]
        nxt=tangents[min(i,len(tangents)-1)]
        n0,n1=(-prev[1],prev[0]),(-nxt[1],nxt[0])
        divisor=1+n0[0]*n1[0]+n0[1]*n1[1]
        miters.append(((n0[0]+n1[0])*5/divisor,(n0[1]+n1[1])*5/divisor))
    outer=[(p[0]+m[0],p[1]+m[1]) for p,m in zip(nodes,miters)]
    inner=[(p[0]-m[0],p[1]-m[1]) for p,m in zip(nodes,miters)]

    def lerp(a,b,t):
        return (a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t)

    def triangle(parent, points, bottom, top, tint):
        # Project the remaining vertex onto the longest side. Both sub-triangles
        # are right triangles representable by one Roblox WedgePart each.
        lengths=[math.dist(points[i],points[(i+1)%3]) for i in range(3)]
        index=max(range(3),key=lambda i:lengths[i])
        a,b,c=points[index],points[(index+1)%3],points[(index+2)%3]
        direction=unit(a,b)
        projection=(c[0]-a[0])*direction[0]+(c[1]-a[1])*direction[1]
        q=(a[0]+direction[0]*projection,a[1]+direction[1]*projection)
        altitude=math.dist(c,q)
        if altitude<1e-7:
            return
        yy=((c[0]-q[0])/altitude,(c[1]-q[1])/altitude)
        for low in (a,b):
            length=math.dist(low,q)
            if length<1e-7:
                continue
            zz=unit(low,q)
            # Local X is vertical; choose its sign so the frame is right-handed.
            vertical=yy[1]*zz[0]-yy[0]*zz[1]
            roll=90 if vertical>0 else -90
            pitch=math.degrees(math.atan2(yy[1],zz[1]))
            part(parent, "MiteredStonePrism", ((low[0]+c[0])/2,(top+bottom)/2,(low[1]+c[1])/2),
                 (top-bottom,altitude,length), tint,"plaster",(pitch,0,roll),cls="WedgePart")

    def band(parent, name, a,b,c,d,bottom,top,tint):
        model=obj(parent,"Model",name)
        triangle(model,(a,b,c),bottom,top,tint)
        triangle(model,(a,c,d),bottom,top,tint)
        return model

    for i,(a,b) in enumerate(zip(nodes,nodes[1:])):
        section=obj(fort,"Model",f'Curtain_{i:02}')
        band(section,'CurtainVolume',inner[i],inner[i+1],outer[i+1],outer[i],-2,22,stone)
        band(section,'OuterParapet',lerp(inner[i],outer[i],.80),lerp(inner[i+1],outer[i+1],.80),
             outer[i+1],outer[i],22,24,cap)
        band(section,'InnerParapet',inner[i],inner[i+1],lerp(inner[i+1],outer[i+1],.12),
             lerp(inner[i],outer[i],.12),22,24,cap)
        # Short merlons sit above, not inside, the continuous parapet.
        direction=tangents[i]
        length=math.dist(a,b)
        normal=(-direction[1],direction[0])
        yaw=-math.degrees(math.atan2(direction[1],direction[0]))
        for k in range(max(1,int(length/8))):
            t=(k+.5)/max(1,int(length/8))
            center=lerp(a,b,t)
            part(section,'PerimeterMerlon',(center[0]+normal[0]*4,25.5,center[1]+normal[1]*4),
                 (3.8,3,2),cap,'plaster',(0,yaw,0))

    # Six solid, seaward bastions. Their decks are above the wall deck, so their
    # foundations do not add a second coincident surface on the wall walk.
    for tower_index,angle in enumerate((63,108,153,198,243,288)):
        i=2+(angle-45)//9
        x,z=nodes[i]
        mx,mz=miters[i]
        normal=mx/math.hypot(mx,mz),mz/math.hypot(mx,mz)
        x,z=x+normal[0]*15,z+normal[1]*15
        tower=obj(fort,'Model',f'Bastion_{tower_index+1:02}')
        disc(tower,'BastionCore',x,8,z,10.5,48,stone,'plaster')
        disc(tower,'BastionCorbel',x,32.5,z,11.5,1,cap,'plaster')
        for y in (9,24):
            disc(tower,'BastionBelt',x,y,z,10.9,1,(123,131,132),'plaster')
        for k in range(10):
            a=k*math.tau/10
            part(tower,'BastionMerlon',(x+10*math.sin(a),35,z+10*math.cos(a)),(3.8,4,2.2),
                 cap,'plaster',(0,k*36,0))
        pole=part(tower,'StandardPole',(x,40,z),(.45,14,.45),(69,76,80),'metal',collide=False)
        prop(pole,'bool','CanQuery',False)
        banner=part(tower,'BastionStandard',(x+2.2,42,z),(4.4,6,.15),(61,82,96),'fabric',collide=False)
        prop(banner,'bool','CanQuery',False)

    access=obj(fort,'Model','RampartAccess')
    for side in (-1,1):
        part(access,'FrontOuterParapet',(side*77.5,23,199),(73,2,2),cap,'plaster')
        # Keep a six-stud opening in the inside rail for the stair landing.
        for start,end in ((41,103.5),(110,114)):
            part(access,'FrontInnerParapet',(side*(start+end)/2,23,190.6),(end-start,2,1.2),cap,'plaster')
        stairs=obj(access,'Model','WestStair' if side<0 else 'EastStair')
        for k in range(14):
            height=k+1
            part(stairs,'RampartTread',(side*(70+(k+.5)*2.5),8+height/2,187),
                 (2.5,height,5),stone,'plaster')
        part(stairs,'RampartLanding',(side*106.5,21.5,188.5),(3,1,3),stone,'plaster')
    return fort
