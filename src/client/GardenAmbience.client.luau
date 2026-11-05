-- Local petal pool and waterfall spray; no gameplay or network state.
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local Workspace = game:GetService("Workspace")
local settings = UserSettings():GetService("UserGameSettings")
local player = Players.LocalPlayer
local map = Workspace:WaitForChild("Archipelago")
local sources, sprays, petals = {}, {}, {}
local time, elapsed = 0, 0
local rng = Random.new(6445)
local folder = Instance.new("Folder")
folder.Name = "LocalGardenAmbience"
folder.Parent = Workspace

local function budget()
    local level = settings.SavedQualityLevel.Value
    if level > 0 and level <= 3 then return 0 end
    return level == 0 and 4 or 8
end

local function register(item)
    if not item:IsA("BasePart") then return end
    if item.Name == "ArtPetalSource" then
        sources[item] = true
    elseif item.Name == "ArtWaterfallMist" and not sprays[item] then
        local spray = Instance.new("ParticleEmitter")
        spray.Name = "LocalWaterfallSpray"
        spray.Texture = "rbxasset://textures/particles/smoke_main.dds"
        spray.Rate = budget() > 0 and 3 or 0
        spray.Lifetime = NumberRange.new(0.8, 1.2)
        spray.Speed = NumberRange.new(1, 3)
        spray.EmissionDirection = Enum.NormalId.Top
        spray.SpreadAngle = Vector2.new(50, 50)
        spray.Size = NumberSequence.new({NumberSequenceKeypoint.new(0, 2), NumberSequenceKeypoint.new(1, 7)})
        spray.Transparency = NumberSequence.new({NumberSequenceKeypoint.new(0, 0.8), NumberSequenceKeypoint.new(1, 1)})
        spray.Color = ColorSequence.new(Color3.fromRGB(179, 225, 234))
        spray.LightInfluence = 0.3
        spray.Parent = item
        sprays[item] = spray
    end
end
for _, item in ipairs(map:GetDescendants()) do register(item) end
local added = map.DescendantAdded:Connect(register)
local removing = map.DescendantRemoving:Connect(function(item)
    sources[item] = nil
    local spray = sprays[item]
    if spray then spray:Destroy(); sprays[item] = nil end
end)

for i = 1, 8 do
    local petal = Instance.new("Part")
    petal.Name = "DriftingPetal"
    petal.Shape = Enum.PartType.Ball
    petal.Size = Vector3.new(0.9, 0.1, 0.4)
    petal.Material = Enum.Material.SmoothPlastic
    petal.Color = Color3.fromRGB(230, 151 + i * 3, 181 + i * 2)
    petal.Anchored = true
    petal.CanCollide = false
    petal.CanTouch = false
    petal.CanQuery = false
    petal.CastShadow = false
    petal.Transparency = 1
    petal.Parent = folder
    table.insert(petals, { Part = petal, Seed = rng:NextNumber(0, 100), Speed = rng:NextNumber(2.1, 3.4) })
end

local changed = settings:GetPropertyChangedSignal("SavedQualityLevel"):Connect(function()
    for _, spray in pairs(sprays) do
        spray.Rate = budget() > 0 and 3 or 0
        if budget() == 0 then spray:Clear() end
    end
end)

local heartbeat = RunService.Heartbeat:Connect(function(dt)
    elapsed = elapsed + dt
    if elapsed < 0.05 then return end
    time = time + elapsed
    elapsed = 0
    local character = player.Character
    local root = character and character:FindFirstChild("HumanoidRootPart")
    local nearest, distance = nil, 130
    if root then
        for source in pairs(sources) do
            if source.Parent then
                local delta = source.Position - root.Position
                local flat = Vector2.new(delta.X, delta.Z).Magnitude
                if flat < distance then nearest, distance = source, flat end
            end
        end
    end
    local count = root and budget() or 0
    for i, petal in ipairs(petals) do
        if nearest and i <= count then
            local source = nearest.Position
            local drop = math.max(8, source.Y - 10)
            local age = (time * petal.Speed + petal.Seed) % drop
            petal.Part.Transparency = 0.12
            petal.Part.CFrame = CFrame.new(source.X + math.sin(time * 0.3 + petal.Seed) * 15,
                source.Y - age, source.Z + math.cos(time * 0.23 + petal.Seed) * 14)
                * CFrame.Angles(math.sin(time + i) * 0.8, time * 0.4 + i, math.cos(time * 0.7 + i) * 0.7)
        else
            petal.Part.Transparency = 1
        end
    end
end)

script.Destroying:Connect(function()
    heartbeat:Disconnect()
    changed:Disconnect()
    added:Disconnect()
    removing:Disconnect()
    for _, spray in pairs(sprays) do spray:Destroy() end
    folder:Destroy()
end)
