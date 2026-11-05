#!/usr/bin/env python3
"""Execute the real weather controller in a small Roblox-API mock with Luau.

This tests state transitions/lifecycle, not Roblox rendering or particle physics.
Usage: python3 tools/check_weather_client.py /path/to/luau
"""
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[1]
luau = sys.argv[1] if len(sys.argv) > 1 else 'luau'
mock = r'''
local function signal()
    local s = {listeners = {}}
    function s:Connect(callback)
        local listener = {Active = true, Callback = callback}
        function listener:Disconnect() self.Active = false end
        table.insert(self.listeners, listener)
        return listener
    end
    function s:Fire(...)
        for _, listener in ipairs(self.listeners) do
            if listener.Active then listener.Callback(...) end
        end
    end
    return s
end
local vectorMeta = {}
local function vector(x,y,z) return setmetatable({X=x,Y=y,Z=z}, vectorMeta) end
vectorMeta.__add = function(a,b) return vector(a.X+b.X,a.Y+b.Y,a.Z+b.Z) end
vectorMeta.__mul = function(a,b)
    if type(b) == "number" then return vector(a.X*b,a.Y*b,a.Z*b) end
    return vector(a.X*b.X,a.Y*b.Y,a.Z*b.Z)
end
vectorMeta.__index = function(a,k)
    if k == "Magnitude" then return math.sqrt(a.X*a.X+a.Y*a.Y+a.Z*a.Z) end
    if k == "Unit" then return a * (1/a.Magnitude) end
end
local Vector3 = {new=vector}
local Vector2 = {new=function(...) return {...} end}
local colorMeta = {}
function colorMeta:Lerp(b,t) return setmetatable({self[1]+(b[1]-self[1])*t,self[2]+(b[2]-self[2])*t,self[3]+(b[3]-self[3])*t}, {__index=colorMeta}) end
local function color(a,b,c) return setmetatable({a,b,c}, {__index=colorMeta}) end
local Color3 = {new=color,fromRGB=function(a,b,c) return color(a/255,b/255,c/255) end}
local sequence = {new=function(...) return {...} end}
local NumberRange, NumberSequence, NumberSequenceKeypoint, ColorSequence = sequence,sequence,sequence,sequence
local Enum = {NormalId={Top="Top"}}
local objects = {}
local Instance = {}
function Instance.new(class)
    local object = {ClassName=class, Clears=0, Destroyed=false}
    function object:Clear() self.Clears = self.Clears + 1 end
    function object:Destroy() self.Destroyed = true end
    table.insert(objects, object)
    return object
end
local heartbeat, qualityChanged, characterAdded = signal(),signal(),signal()
local settings = {SavedQualityLevel={Value=QUALITY}}
function settings:GetPropertyChangedSignal(_) return qualityChanged end
local function UserSettings() return {GetService=function() return settings end} end
local atmosphere = {Density=.29,Haze=1.9,Offset=.05,Color=color(.75,.81,.84)}
local character = {Root={Position=vector(0,10,0)}}
function character:FindFirstChild(_) return self.Root end
local player = {Character=character,CharacterAdded=characterAdded}
local camera = {CFrame={LookVector=vector(0,0,-1)}}
local services = {
    Players={LocalPlayer=player},
    RunService={Heartbeat=heartbeat},
    Workspace={CurrentCamera=camera},
    Lighting={WaitForChild=function() return atmosphere end},
    ReplicatedStorage={WaitForChild=function() return "WorldEnvironment" end},
}
local game = {GetService=function(_,key) return services[key] end}
local script = {Destroying=signal()}
local function require(_) return worldConfig end
'''
checks = r'''
local function frames(n) for _=1,n do heartbeat:Fire(.1) end end
local function allStopped()
    for _, o in ipairs(objects) do
        if o.ClassName == "ParticleEmitter" then assert(o.Rate == 0, "Mist did not stop") end
    end
end
frames(10)
assert(math.abs(atmosphere.Density-.29)<.001)
allStopped()
character.Root.Position=vector(2300,10,0)
frames(100)
assert(atmosphere.Density>.388 and atmosphere.Haze>2.99, "Ocean atmosphere did not strengthen")
local emitted=false
for _,o in ipairs(objects) do
    if o.ClassName=="ParticleEmitter" then emitted=emitted or o.Rate>0 end
end
assert(emitted == (QUALITY>3 or QUALITY==0), "Quality particle budget failed")
settings.SavedQualityLevel.Value=2
qualityChanged:Fire()
frames(2)
allStopped()
settings.SavedQualityLevel.Value=8
qualityChanged:Fire()
frames(2)
player.Character=nil
frames(2)
allStopped()
assert(atmosphere.Density==.29, "Fog survived missing character")
player.Character=character
character.Root.Position=vector(0,10,0)
characterAdded:Fire(character)
assert(atmosphere.Density==.29, "Fog survived respawn")
frames(20)
allStopped()
services.Workspace.CurrentCamera=nil
frames(2)
services.Workspace.CurrentCamera=camera
camera.CFrame.LookVector=vector(0,1,0)
character.Root.Position=vector(2300,10,0)
frames(100)
assert(atmosphere.Density>.388, "Vertical camera handling failed")
script.Destroying:Fire()
local frozen=atmosphere.Density
character.Root.Position=vector(0,10,0)
frames(10)
assert(atmosphere.Density==frozen, "Heartbeat survived cleanup")
for _,o in ipairs(objects) do
    if o.ClassName=="Part" then assert(o.Destroyed, "Mist anchor leaked") end
end
print("Weather client: land/ocean, quality changes, missing camera/character, respawn, vertical camera and cleanup passed; quality="..QUALITY)
'''
with tempfile.TemporaryDirectory(prefix='harbor-weather-') as folder:
    for quality in (0, 2, 8):
        script = Path(folder)/f'weather-{quality}.luau'
        source = (f'local QUALITY={quality}\nlocal worldConfig = (function()\n'
                  +(root/'src/shared/WorldEnvironment.luau').read_text()+'\nend)()\n'
                  +mock+'\n'+(root/'src/client/MaritimeWeather.client.luau').read_text()+'\n'+checks)
        script.write_text(source)
        subprocess.run([luau, str(script)], check=True)
