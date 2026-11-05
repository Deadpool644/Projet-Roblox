-- Water is native Roblox Terrain so future boats and swimming use real water.
-- The thin ocean part exists only to make the map readable in edit mode.
local Workspace = game:GetService("Workspace")
local map = Workspace:WaitForChild("Archipelago")
local preview = map:FindFirstChild("OceanPreview")

Workspace.Terrain.WaterColor = Color3.fromRGB(39, 78, 91)
Workspace.Terrain.WaterTransparency = 0.3
Workspace.Terrain.WaterReflectance = 0.15
Workspace.Terrain.WaterWaveSize = 0.15
Workspace.Terrain.WaterWaveSpeed = 8
-- Chunking avoids a single large blocking terrain operation at startup.
for x = -2688, 2688, 768 do
	for z = -2688, 2688, 768 do
		Workspace.Terrain:FillBlock(CFrame.new(x, -8, z), Vector3.new(768, 16, 768), Enum.Material.Water)
	end
	task.wait()
end

if preview then
	preview:Destroy()
end
