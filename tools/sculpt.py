"""Original sculpted scenery using native geometry; no uploaded mesh dependencies."""
import math


class Sculpt:
    def __init__(self, *, obj, part, disc, prop, color):
        self.obj, self.part, self.disc, self.prop, self.color = obj, part, disc, prop, color

    def group(self, parent, name):
        return self.obj(parent, "Model", name)

    def p(self, parent, name, pos, size, tint, material="plastic", rotation=(0,0,0), solid=False, shape=1):
        item=self.part(parent,name,pos,size,tint,material,rotation,shape,collide=solid)
        if not solid:
            self.prop(item,"bool","CanQuery",False)
        if max(size)<6 or min(size)<.5:
            self.prop(item,"bool","CastShadow",False)
        return item

    def ball(self,parent,name,pos,size,tint,material="plastic",rotation=(0,0,0),solid=False):
        return self.p(parent,name,pos,size,tint,material,rotation,solid,0)

    def rod(self,parent,name,a,b,width,tint,material="wood",solid=False):
        dx,dy,dz=(b[i]-a[i] for i in range(3))
        length=math.sqrt(dx*dx+dy*dy+dz*dz)
        return self.p(parent,name,tuple((a[i]+b[i])/2 for i in range(3)),(length,width,width),tint,material,
                      (0,-math.degrees(math.asin(dz/length)),math.degrees(math.atan2(dy,dx))),solid,2)

    def triangle_xy(self,parent,name,points,z,depth,tint,material="plaster"):
        lengths=[math.dist(points[i],points[(i+1)%3]) for i in range(3)]
        i=max(range(3),key=lambda j:lengths[j])
        a,b,c=points[i],points[(i+1)%3],points[(i+2)%3]
        direction=((b[0]-a[0])/lengths[i],(b[1]-a[1])/lengths[i])
        d=(c[0]-a[0])*direction[0]+(c[1]-a[1])*direction[1]
        q=(a[0]+direction[0]*d,a[1]+direction[1]*d)
        altitude=math.dist(q,c)
        if altitude<1e-7:return
        yy=((c[0]-q[0])/altitude,(c[1]-q[1])/altitude)
        for low in (a,b):
            length=math.dist(low,q)
            if length<1e-7:continue
            zz=((q[0]-low[0])/length,(q[1]-low[1])/length)
            normal=yy[0]*zz[1]-yy[1]*zz[0]
            item=self.part(parent,name,((low[0]+c[0])/2,(low[1]+c[1])/2,z),
                           (depth,altitude,length),tint,material,cls="WedgePart")
            frame=item.find("Properties/CoordinateFrame[@name='CFrame']")
            columns=((0,0,normal),(yy[0],yy[1],0),(zz[0],zz[1],0))
            for row in range(3):
                for col in range(3):frame.find(f'R{row}{col}').text=str(round(columns[col][row],6))

    def quad_xy(self,parent,name,a,b,c,d,z,depth,tint,material="plaster"):
        self.triangle_xy(parent,name,(a,b,c),z,depth,tint,material)
        self.triangle_xy(parent,name,(a,c,d),z,depth,tint,material)

    def anchor(self,parent,name,pos):
        item=self.p(parent,name,pos,(1,1,1),(0,0,0))
        self.prop(item,"float","Transparency",1)
        return item

    def light(self,parent,tint,range_=30,brightness=1.4):
        light=self.obj(parent,"PointLight","ArtLight")
        self.prop(light,"float","Range",range_)
        self.prop(light,"float","Brightness",brightness)
        self.prop(light,"bool","Shadows",False)
        self.color(light,"Color",tint)
        return light

    @staticmethod
    def name(item):
        return item.find("Properties/string[@name='Name']").text

    @staticmethod
    def position(item):
        f=item.find("Properties/CoordinateFrame[@name='CFrame']")
        return tuple(float(f.find(k).text) for k in ('X','Y','Z'))

    @staticmethod
    def translate(item,delta):
        f=item.find("Properties/CoordinateFrame[@name='CFrame']")
        for k,d in zip(('X','Y','Z'),delta):f.find(k).text=str(float(f.find(k).text)+d)

    @staticmethod
    def recolor(item,tint):
        node=item.find("Properties/Color3[@name='Color']")
        for k,c in zip(('R','G','B'),tint):node.find(k).text=str(c/255)
