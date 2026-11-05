#!/usr/bin/env python3
"""Run the real garden controller under Luau with mocked APIs, not native rendering."""
from pathlib import Path
import subprocess
import sys
import tempfile

root=Path(__file__).resolve().parents[1]
luau=sys.argv[1] if len(sys.argv)>1 else 'luau'
mock=r'''
local function signal()
    local s={listeners={}}
    function s:Connect(cb)
        local c={Active=true,Callback=cb}
        function c:Disconnect() self.Active=false end
        table.insert(self.listeners,c)
        return c
    end
    function s:Fire(...)
        for _,c in ipairs(self.listeners) do if c.Active then c.Callback(...) end end
    end
    return s
end
local vm={}
local function vector(x,y,z) return setmetatable({X=x,Y=y,Z=z},vm) end
vm.__sub=function(a,b) return vector(a.X-b.X,a.Y-b.Y,a.Z-b.Z) end
local Vector3={new=vector}
local Vector2={new=function(x,y) return {Magnitude=math.sqrt(x*x+y*y)} end}
local sequence={new=function(...) return {...} end}
local NumberRange,NumberSequence,NumberSequenceKeypoint,ColorSequence=sequence,sequence,sequence,sequence
local Color3={fromRGB=function(...) return {...} end}
local Enum={PartType={Ball=0},Material={SmoothPlastic=272},NormalId={Top=1}}
local cf={__mul=function(a,b) return a end}
local CFrame={new=function(...) return setmetatable({...},cf) end,Angles=function(...) return setmetatable({...},cf) end}
local Random={new=function(seed)
    return {Seed=seed,NextNumber=function(self,a,b)
        self.Seed=self.Seed*16807%2147483647
        return a+(b-a)*self.Seed/2147483647
    end}
end}
local objects={}
local Instance={}
function Instance.new(class)
    local o={ClassName=class,Destroyed=false,Clears=0}
    function o:Destroy()
        self.Destroyed=true
        for _,child in ipairs(objects) do if child.Parent==self and not child.Destroyed then child:Destroy() end end
    end
    function o:Clear() self.Clears=self.Clears+1 end
    function o:IsA(kind) return kind==self.ClassName or kind=='BasePart' and self.ClassName=='Part' end
    table.insert(objects,o)
    return o
end
local heartbeatEvent,qualityChanged=signal(),signal()
local settings={SavedQualityLevel={Value=QUALITY}}
function settings:GetPropertyChangedSignal() return qualityChanged end
local function UserSettings() return {GetService=function() return settings end} end
local map={DescendantAdded=signal(),DescendantRemoving=signal()}
local source=Instance.new('Part')
source.Name='ArtPetalSource';source.Position=vector(-42,56,-192);source.Parent=map
local mist=Instance.new('Part')
mist.Name='ArtWaterfallMist';mist.Position=vector(150,10,-163);mist.Parent=map
function map:GetDescendants() return {source,mist} end
local character={Root={Position=vector(0,10,0)}}
function character:FindFirstChild() return self.Root end
local player={Character=character}
local services={Players={LocalPlayer=player},RunService={Heartbeat=heartbeatEvent},Workspace={WaitForChild=function() return map end}}
local game={GetService=function(_,key) return services[key] end}
local script={Destroying=signal()}
'''
checks=r'''
local function frames(n) for _=1,n do heartbeatEvent:Fire(.05) end end
local function visible()
    local n=0
    for _,o in ipairs(objects) do if o.Name=='DriftingPetal' and o.Transparency<1 then n=n+1 end end
    return n
end
frames(2)
assert(visible()==0,'Petals emitted outside garden')
character.Root.Position=vector(-42,10,-192)
frames(4)
assert(visible()==(QUALITY==0 and 4 or QUALITY<=3 and 0 or 8),'Incorrect visual quality budget')
settings.SavedQualityLevel.Value=2;qualityChanged:Fire();frames(2)
assert(visible()==0,'Low-quality petals not hidden')
settings.SavedQualityLevel.Value=8;qualityChanged:Fire();frames(2)
assert(visible()==8,'Pool not reused')
map.DescendantRemoving:Fire(source);source.Parent=nil;frames(2)
assert(visible()==0,'Streamed-out source still active')
source.Parent=map;map.DescendantAdded:Fire(source);frames(2)
assert(visible()==8,'Streamed-in source not registered')
map.DescendantRemoving:Fire(mist);mist.Parent=nil
mist.Parent=map;map.DescendantAdded:Fire(mist)
local activeSpray=0
for _,o in ipairs(objects) do if o.ClassName=='ParticleEmitter' and not o.Destroyed then activeSpray=activeSpray+1 end end
assert(activeSpray==1,'Waterfall emitter leaked across streaming')
player.Character=nil;frames(2)
assert(visible()==0,'Petals visible without character')
script.Destroying:Fire()
for _,o in ipairs(objects) do
    if o.Name=='DriftingPetal' or o.ClassName=='ParticleEmitter' then assert(o.Destroyed,'Visual instance leaked') end
end
print('Garden client passed: proximity, quality '..QUALITY..', pooled petals, streaming, absent character and cleanup')
'''
with tempfile.TemporaryDirectory(prefix='garden-check-') as directory:
    for quality in (0,2,8):
        path=Path(directory)/f'check-{quality}.luau'
        path.write_text(f'local QUALITY={quality}\n'+mock+'\n'+(root/'src/client/GardenAmbience.client.luau').read_text()+'\n'+checks)
        subprocess.run([luau,str(path)],check=True)
