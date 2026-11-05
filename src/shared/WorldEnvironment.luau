-- Generated from tools/world.json by tools/build_map.py.
local WorldEnvironment = {}
WorldEnvironment.Islands = {
    { X = 0, Z = 0, Radius = 296.00, DockZ = 290 },
    { X = 0, Z = 850, Radius = 176.00, DockZ = 1040 },
    { X = -850, Z = 0, Radius = 176.00, DockZ = 190 },
    { X = 850, Z = 0, Radius = 176.00, DockZ = 190 },
    { X = 0, Z = -850, Radius = 176.00, DockZ = -660 },
    { X = -1080, Z = 1320, Radius = 212.00, DockZ = 1540 },
    { X = 1080, Z = 1320, Radius = 212.00, DockZ = 1540 },
    { X = 1640, Z = -480, Radius = 212.00, DockZ = -260 },
    { X = 0, Z = -1700, Radius = 212.00, DockZ = -1480 },
    { X = -1640, Z = -480, Radius = 212.00, DockZ = -260 },
    { X = -1900, Z = 1900, Radius = 248.00, DockZ = 2150 },
    { X = 1900, Z = 1900, Radius = 248.00, DockZ = 2150 },
    { X = -1900, Z = -1900, Radius = 248.00, DockZ = -1650 },
    { X = 1900, Z = -1900, Radius = 248.00, DockZ = -1650 },
}

-- Smooth transition: no ocean fog while on any island or its quay.
function WorldEnvironment.SeaWeight(x, z)
    local nearest = math.huge
    for _, island in ipairs(WorldEnvironment.Islands) do
        local dx, dz = x - island.X, z - island.Z
        nearest = math.min(nearest, math.sqrt(dx * dx + dz * dz) - island.Radius)
        local qx = math.max(math.abs(dx) - 60, 0)
        local qz = math.max(math.abs(z - island.DockZ) - 60, 0)
        nearest = math.min(nearest, math.sqrt(qx * qx + qz * qz))
    end
    local t = math.clamp((nearest - 35) / 260, 0, 1)
    return t * t * (3 - 2 * t)
end

return WorldEnvironment
