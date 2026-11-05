"""Grand Port art pass: original monumental gateway and flowering coastal gardens."""
import math
import random
from sculpt import Sculpt


def art_pass(hub, *, obj, part, disc, prop, color):
    s=Sculpt(obj=obj,part=part,disc=disc,prop=prop,color=color)
    rng=random.Random(202611051)
    art=s.group(hub,"CinematicGardens")
    stone=(84,101,123)
    trim=(144,153,158)
    metal=(39,48,64)
    gold=(182,142,77)
    wood=(73,48,43)

    # Cool, carved masonry; the complementary warm color comes from the lanterns.
    fort=next(i for i in hub.findall('Item') if s.name(i)=='IslandFortress')
    for item in fort.findall('.//Item'):
        if item.get('class') not in ('Part','WedgePart'):continue
        if s.name(item) in ('MiteredStonePrism','BastionCore'):
            s.recolor(item,stone)
        elif s.name(item) in ('BastionCorbel','BastionBelt','BastionMerlon','PerimeterMerlon'):
            s.recolor(item,trim)

    gate=s.group(art,'MonumentalGate')
    old=next(i for i in hub.findall('Item') if s.name(i)=='HarborFortifications')
    for item in old.findall('Item'):
        if s.name(item)=='GateTower':
            frame=item.find("Properties/CoordinateFrame[@name='CFrame']")
            frame.find('Y').text='37'
            item.find("Properties/Vector3[@name='size']/Y").text='58'  # 8..66
            s.recolor(item,stone)
        elif s.name(item)=='TowerCrown':
            s.translate(item,(0,28,0))
            s.recolor(item,trim)

    # One polygonal arch profile; its spandrels use precisely the same outer edge.
    inner_radius,outer_radius,spring=21,25,28
    for k in range(12):
        a,b=k*math.pi/12,(k+1)*math.pi/12
        ia=(inner_radius*math.cos(a),spring+inner_radius*math.sin(a))
        ib=(inner_radius*math.cos(b),spring+inner_radius*math.sin(b))
        oa=(outer_radius*math.cos(a),spring+outer_radius*math.sin(a))
        ob=(outer_radius*math.cos(b),spring+outer_radius*math.sin(b))
        s.quad_xy(gate,'ArchVoussoir',ia,ib,ob,oa,195,14,(129+k%3*4,139+k%3*4,147+k%3*4))
        low,high=sorted((oa,ob))
        left,right=max(-21,low[0]),min(21,high[0])
        if right-left>1e-6:
            def height(x):return low[1]+(high[1]-low[1])*(x-low[0])/(high[0]-low[0])
            s.quad_xy(gate,'ArchSpandrel',(left,height(left)),(right,height(right)),(right,66),(left,66),195,14,stone)
    s.p(gate,'BridgeCornice',(0,67,195),(44,2,16),trim,'plaster',solid=True)
    for x in range(-18,19,9):
        s.p(gate,'GateBridgeMerlon',(x,70,200),(4,4,2),trim,'plaster',solid=True)
    for side in (-1,1):
        x=side*31
        s.p(gate,'TowerRoofCap',(x,70.5,188),(22,1,26),trim,'plaster',solid=True)
        for dx in (-8,0,8):
            for z in (177,199):
                s.p(gate,'GateCrownMerlon',(x+dx,73.5,z),(4,5,3),trim,'plaster',solid=True)
        # Freestanding pier accents are wholly outside the existing tower faces.
        for dx in (-8.3,8.3):
            s.p(gate,'TowerFrontPilaster',(x+dx,37,201),(2.5,58,1.5),trim,'plaster')
        for y in (12,37,64):
            s.p(gate,'TowerFrontBand',(x,y,201.9),(20,1,1),gold,'metal')
        # Braseros are visual fire; they do not damage characters.
        s.rod(gate,'TorchBracket',(x,18,201),(x,21,205),.7,metal,'metal')
        bowl=s.ball(gate,'GateBrazier',(x,22,205),(3,1.2,3),metal,'metal')
        flame=s.obj(bowl,'Fire','WarmGateFire')
        s.prop(flame,'float','Size',5)
        s.prop(flame,'float','Heat',5)
        s.color(flame,'Color',(255,174,72))
        s.color(flame,'SecondaryColor',(222,83,47))
        s.light(bowl,(255,174,92),36,1.7)
        for j in range(5):
            a=j*math.tau/5
            s.rod(gate,'BrazierProng',(x+1.1*math.sin(a),22,205+1.1*math.cos(a)),
                  (x+1.5*math.sin(a),24,205+1.5*math.cos(a)),.25,metal,'metal')

        # Alternating interlinked ellipses follow a sagged path above the rampart.
        chain=s.group(gate,'WestAnchorChain' if side<0 else 'EastAnchorChain')
        count=16
        for link in range(count):
            t=(link+.5)/count
            cx,cy,cz=side*(42+70*t),66-33*t-56*t*(1-t),204
            tangent=(side*70,-89+112*t,0)
            length=math.hypot(tangent[0],tangent[1])
            u=(tangent[0]/length,tangent[1]/length,0)
            v=(-u[1],u[0],0) if link%2==0 else (0,0,1)
            points=[]
            for j in range(8):
                a=j*math.tau/8
                points.append(tuple((cx,cy,cz)[i]+u[i]*2.8*math.cos(a)+v[i]*1.7*math.sin(a) for i in range(3)))
            for a,b in zip(points,points[1:]+points[:1]):s.rod(chain,'ForgedChainLink',a,b,.7,metal,'metal')

    # Original compass crest, rather than a logo copied from the reference.
    crest=s.p(gate,'GateCrest',(0,56.5,203),(1,11.4,11.4),metal,'metal',(0,90,0),shape=2)
    for k in range(8):
        a=k*math.tau/8
        b=(k+1)*math.tau/8
        s.rod(gate,'CrestRing',(5*math.cos(a),56.5+5*math.sin(a),203.7),
              (5*math.cos(b),56.5+5*math.sin(b),203.7),.25,gold,'metal')
    for k in range(4):
        a=k*math.pi/2
        end=(math.sin(a)*4.1,56.5+math.cos(a)*4.1,204)
        s.rod(gate,'CompassRay',(0,56.5,204),end,.6,gold,'metal')

    ivy=s.group(gate,'GateIvy')
    for side in (-1,1):
        previous=(side*38,61,203)
        for k in range(9):
            current=(side*(38+math.sin(k*.7)*1.3),61-k*3,203)
            if k:s.rod(ivy,'IvyStem',previous,current,.15,(53,83,63))
            for leaf in (-1,1):
                s.ball(ivy,'IvyLeaf',(current[0]+leaf*1.2,current[1]-.6,203.2),(2.8,.18,1.5),
                       (53+k%3*6,106+k%3*8,79+k%3*4),rotation=(90,0,leaf*24))
            previous=current

    # Mount the existing physical port sign on the new bridge, keeping its lettering.
    square=next(i for i in hub.findall('.//Item') if s.name(i)=='CivicSquare')
    for item in square.findall('Item'):
        if item.get('class')!='Part':continue
        x,y,z=s.position(item)
        if (s.name(item) in ('CarvedSign','SignBorder') and abs(x)<.01 and 180<z<193) or s.name(item)=='GateSignChain':
            s.translate(item,(0,39,12))

    # Distinct, restrained roof palettes and carved ridge terminals.
    palettes={'ARMES':(57,79,101),'ARMURES':(56,75,96),'FRUITS':(111,57,76),
              'GUILDE DES PIRATES':(90,51,61),'QUARTIER MARINE':(53,79,101),
              'CHANTIER NAVAL':(101,77,60),'MARCHÉ':(112,61,73),'MISSIONS / TUTORIEL':(61,82,103)}
    for building in hub.findall('Item'):
        if s.name(building) not in palettes:continue
        tint=palettes[s.name(building)]
        for item in building.findall('.//Item'):
            if item.get('class')=='Part' and s.name(item) in ('RoofSlope','SlateCourse'):
                s.recolor(item,tint)
        roof=next(i for i in building.findall('.//Item') if s.name(i)=='RoofAssembly')
        values={s.name(i):float(i.find("Properties/double[@name='Value']").text) for i in roof.findall("Item[@class='NumberValue']")}
        for end in (-1,1):
            x,y,z=values['CenterX'],values['RidgeHeight']+.65,values['CenterZ']+end*(values['Depth']/2+4)
            s.rod(gate,'CarvedRoofTerminal',(x,y,z),(x,y+2,z+end*3),1.1,wood)
            s.ball(gate,'GildedRoofTip',(x,y+2,z+end*3),(1.2,1.2,1.2),gold,'metal')

    # Remove the hub's original plank-like palm silhouettes; keep the existing oaks.
    for item in list(hub.findall('Item')):
        if s.name(item) in ('Trunk','PalmFrond'):hub.remove(item)

    gardens=s.group(art,'FloweringGardens')
    def sakura(x,z,scale):
        tree=s.group(gardens,'FloweringTree')
        points=[(x,8,z),(x+3*scale,8+14*scale,z-scale),(x+scale,8+30*scale,z+scale),
                (x-4*scale,8+45*scale,z+3*scale)]
        for i,(a,b) in enumerate(zip(points,points[1:])):s.rod(tree,'CurvedTrunk',a,b,(8-i*2)*scale,wood,solid=True)
        for k in range(5):
            a=k*math.tau/5
            s.rod(tree,'TreeRoot',(x+math.cos(a)*8*scale,8.4,z+math.sin(a)*8*scale),(x,12,z),1.5*scale,wood)
        for branch in range(9):
            a=branch*math.tau/9+.2
            reach=rng.uniform(.72,1.12)
            root=(x+scale,8+30*scale,z+scale)
            mid=(x+math.cos(a)*13*scale,8+(40+branch%3*3)*scale,z+math.sin(a)*12*scale)
            tip=(x+math.cos(a)*24*scale*reach,8+(45+branch%3*4+rng.uniform(-2,4))*scale,z+math.sin(a)*22*scale*reach)
            s.rod(tree,'SweepingBranch',root,mid,2.2*scale,wood)
            s.rod(tree,'BranchFork',mid,tip,1.2*scale,wood)
            for layer in range(3):
                cx,cy,cz=tip[0]+rng.uniform(-6,6)*scale,tip[1]+layer*1.8*scale,tip[2]+rng.uniform(-6,6)*scale
                shade=branch%4*9+layer*8
                s.ball(tree,'BlossomMass',(cx,cy,cz),(rng.uniform(13,18)*scale,rng.uniform(9,13)*scale,rng.uniform(11,15)*scale),
                       (163+shade,93+shade//2,134+shade//2),rotation=(rng.uniform(-10,10),branch*39,0))
                # Individual lens-shaped leaves break the broad canopy contour.
                for leaf in range(5):
                    xx,zz=cx+rng.uniform(-8,8)*scale,cz+rng.uniform(-6,6)*scale
                    s.ball(tree,'BlossomLeaf',(xx,cy+rng.uniform(-2,3)*scale,zz),(3.6*scale,.3*scale,1.65*scale),
                           (208+leaf*5,129+shade//2,159+leaf*3),rotation=(rng.uniform(-35,35),rng.uniform(0,360),rng.uniform(-25,25)))
        for k in range(5):
            s.ball(tree,'BlossomMass',(x+rng.uniform(-8,8)*scale,8+(54+k%2*4)*scale,z+rng.uniform(-8,8)*scale),
                   (17*scale,11*scale,15*scale),(177+k*6,105+k*4,141+k*5),rotation=(0,k*43,0))
        s.anchor(tree,'ArtPetalSource',(x,8+43*scale,z))
        # Suspended warm lanterns with rods/frames; no extra dynamic lights.
        for dx in (-9,9):
            ly=8+30*scale
            s.rod(tree,'LanternCord',(x+dx*scale,ly+7*scale,z+8*scale),(x+dx*scale,ly,z+8*scale),.15,wood)
            s.p(tree,'HangingLantern',(x+dx*scale,ly-1.5,z+8*scale),(1.7,3,1.7),(251,193,110),'neon')
            for yy in (-3,0):s.p(tree,'LanternRim',(x+dx*scale,ly+yy,z+8*scale),(2,.3,2),metal,'metal')
    sakura(-42,-192,1.12)
    sakura(167,-85,.82)
    sakura(-166,20,.76)

    green=(42,94,71)
    def fern(parent,x,z,scale=1):
        for k in range(7):
            a=k*math.tau/7
            length=(5+k%3)*scale
            s.ball(parent,'FernFrond',(x+math.sin(a)*length*.4,8.8+length*.13,z+math.cos(a)*length*.4),
                   (1.5*scale,.25*scale,length),(42+k*3,87+k*4,66+k*2),rotation=(18,k*360/7,0))
    plants=s.group(gardens,'UnderstoryAndFlowers')
    for x,z in ((-24,-177),(-61,-179),(-67,-205),(-15,-198),(141,-86),(185,-93),(172,-64),
                (-180,12),(-153,9),(-176,37),(-57,31),(57,31),(-174,120),(180,125),
                (126,-174),(172,-137),(134,-139),(-120,-164),(-65,-87),(54,-89)):
        fern(plants,x,z,rng.uniform(.8,1.3))
    for x,z in ((-27,-177),(-62,-182),(-19,-200),(145,-83),(185,-88),(-179,15),(-154,12),
                (132,-141),(170,-137),(-116,-164),(-56,32),(56,32)):
        for flower in range(3):
            xx,zz=x+flower*1.8,z+flower%2*1.5
            s.rod(plants,'FlowerStem',(xx,8,zz),(xx,10.1,zz),.14,green)
            for petal in range(5):
                a=petal*math.tau/5
                s.ball(plants,'FlowerPetal',(xx+math.sin(a)*.65,10.1,zz+math.cos(a)*.65),
                       (1.1,.18,.65),(205+flower*12,107+flower*20,139+flower*18),rotation=(0,petal*72,0))
            s.ball(plants,'FlowerCenter',(xx,10.2,zz),(.5,.2,.5),(229,182,80))

    cascade=s.group(art,'CascadeGarden')
    # Raised ornamental pool. This is scenery; the ocean remains native swimming water.
    s.ball(cascade,'PoolBed',(150,8.4,-149),(36,1,27),(58,78,87),'slate')
    water=s.ball(cascade,'GardenWater',(150,9,-149),(33,.45,24),(64,153,176),'glass')
    s.prop(water,'float','Transparency',.18)
    s.prop(water,'float','Reflectance',.12)
    for k in range(13):
        a=k*math.tau/13
        s.ball(cascade,'PoolRimRock',(150+math.sin(a)*17,9.2,-149+math.cos(a)*12),
               (5.3,3,4),(87+k%3*6,105+k%3*5,118+k%3*4),'slate',rotation=(0,k*31,10),solid=True)
    for x,y,z,size in ((150,21,-173,(21,27,12)),(134,17,-171,(17,19,13)),(165,19,-171,(15,23,12)),
                       (143,32,-173,(17,9,11)),(162,28,-174,(13,12,12))):
        s.ball(cascade,'WaterfallRock',(x,y,z),size,(72,91,110),'slate',rotation=(0,x%28,8),solid=True)
        s.ball(cascade,'RockMoss',(x,y+size[1]/2-.2,z),(size[0]*.8,1.1,size[2]*.7),(58,97,75),'grass')
    for k in range(6):
        x=146.5+k*1.35
        ribbon=s.p(cascade,'WaterfallRibbon',(x,20,-165.5),(1.25,22,.45),(73+k*6,178+k*5,207+k*5),'glass')
        s.prop(ribbon,'float','Transparency',.25)
        glint=s.p(cascade,'FallingWaterGlint',(x+.3,20,-165.2),(.12,21,.12),(180,232,242),'neon')
        s.prop(glint,'float','Transparency',.65)
    s.anchor(cascade,'ArtWaterfallMist',(150,10,-163))
    glow=s.anchor(cascade,'WaterfallFillLight',(150,16,-159))
    s.light(glow,(105,192,217),24,.65)
    # Navigable stepping stones in front of the ornamental pool; not a required route.
    for x,z in ((134,-150),(138,-144),(142,-140)):
        s.ball(cascade,'GardenSteppingStone',(x,10,z),(5,1.7,4),(131,142,143),'slate',solid=True)
    return art
