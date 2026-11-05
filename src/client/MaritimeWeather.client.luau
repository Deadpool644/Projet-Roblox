-- Local visual treatment only. Never changes server gameplay or global weather.
local Lighting = game:GetService("Lighting")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local Workspace = game:GetService("Workspace")
local world = require(ReplicatedStorage:WaitForChild("WorldEnvironment"))
local atmosphere = Lighting:WaitForChild("HarborAtmosphere")
local player = Players.LocalPlayer

local landColor = Color3.new(0.75, 0.81, 0.84)
local seaColor = Color3.new(0.69, 0.77, 0.81)
local weight = 0
local elapsed = 0
local wasEmitting = false
local anchors = {}
local emitters = {}

local settings = UserSettings():GetService("UserGameSettings")
local quality = settings.SavedQualityLevel.Value
local lowQuality = quality > 0 and quality <= 3
local qualityConnection = settings:GetPropertyChangedSignal("SavedQualityLevel"):Connect(function()
    local level = settings.SavedQualityLevel.Value
    lowQuality = level > 0 and level <= 3
    if lowQuality then
        for _, emitter in ipairs(emitters) do
            emitter.Rate = 0
            emitter:Clear()
        end
    end
end)

for side = -1, 1, 2 do
    local anchor = Instance.new("Part")
    anchor.Name = "LocalSeaMist"
    anchor.Size = Vector3.new(1, 1, 1)
    anchor.Anchored = true
    anchor.Transparency = 1
    anchor.CanCollide = false
    anchor.CanTouch = false
    anchor.CanQuery = false
    anchor.CastShadow = false
    anchor.Parent = Workspace

    local emitter = Instance.new("ParticleEmitter")
    emitter.Name = "LowSeaMist"
    emitter.Texture = "rbxasset://textures/particles/smoke_main.dds"
    emitter.Rate = 0
    emitter.Lifetime = NumberRange.new(6, 8)
    emitter.Speed = NumberRange.new(2, 4)
    emitter.Drag = 0.6
    emitter.EmissionDirection = Enum.NormalId.Top
    emitter.SpreadAngle = Vector2.new(70, 70)
    emitter.Size = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 55),
        NumberSequenceKeypoint.new(0.6, 95),
        NumberSequenceKeypoint.new(1, 120),
    })
    emitter.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 1),
        NumberSequenceKeypoint.new(0.35, 0.95),
        NumberSequenceKeypoint.new(0.7, 0.97),
        NumberSequenceKeypoint.new(1, 1),
    })
    emitter.Color = ColorSequence.new(Color3.fromRGB(178, 198, 206))
    emitter.LightEmission = 0
    emitter.LightInfluence = 0.2
    emitter.Rotation = NumberRange.new(-180, 180)
    emitter.RotSpeed = NumberRange.new(-3, 3)
    emitter.LockedToPart = false
    emitter.Parent = anchor
    table.insert(anchors, { Part = anchor, Side = side })
    table.insert(emitters, emitter)
end

local function resetMist()
    weight = 0
    atmosphere.Density = 0.29
    atmosphere.Haze = 1.9
    atmosphere.Offset = 0.05
    atmosphere.Color = landColor
    for _, emitter in ipairs(emitters) do
        emitter.Rate = 0
        emitter:Clear()
    end
    wasEmitting = false
end
local respawnConnection = player.CharacterAdded:Connect(resetMist)

local connection
connection = RunService.Heartbeat:Connect(function(dt)
    elapsed = elapsed + dt
    if elapsed < 0.1 then
        return
    end
    local step = math.min(elapsed, 0.5)
    elapsed = 0
    local camera = Workspace.CurrentCamera
    local character = player.Character
    local root = character and character:FindFirstChild("HumanoidRootPart")
    if not camera or not root then
        resetMist()
        return
    end

    local target = world.SeaWeight(root.Position.X, root.Position.Z)
    weight = weight + (target - weight) * (1 - math.exp(-step / 1.8))
    atmosphere.Density = 0.29 + weight * 0.10
    atmosphere.Haze = 1.9 + weight * 1.1
    atmosphere.Offset = 0.05 - weight * 0.13
    atmosphere.Color = landColor:Lerp(seaColor, weight)

    local emitting = target > 0.08 and root.Position.Y < 70
    local forward = camera.CFrame.LookVector * Vector3.new(1, 0, 1)
    if forward.Magnitude < 0.01 then
        forward = Vector3.new(0, 0, -1)
    else
        forward = forward.Unit
    end
    local right = Vector3.new(-forward.Z, 0, forward.X)
    for i, anchor in ipairs(anchors) do
        local pos = root.Position + forward * 100 + right * (anchor.Side * 70)
        anchor.Part.Position = Vector3.new(pos.X, 3, pos.Z)
        -- Avoid emitting wisps over another island when sailing close to it.
        local localSea = world.SeaWeight(pos.X, pos.Z)
        emitters[i].Rate = emitting and (lowQuality and 0 or 1.25 * weight * localSea) or 0
        if not emitting and wasEmitting then
            emitters[i]:Clear()
        end
    end
    wasEmitting = emitting
end)

script.Destroying:Connect(function()
    if connection then
        connection:Disconnect()
    end
    qualityConnection:Disconnect()
    respawnConnection:Disconnect()
    for _, anchor in ipairs(anchors) do
        anchor.Part:Destroy()
    end
end)
