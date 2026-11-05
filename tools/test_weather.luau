-- Run with the official Luau CLI from the repository root: luau tools/test_weather.luau
local world = require("../src/shared/WorldEnvironment")
assert(#world.Islands == 14)
for _, island in ipairs(world.Islands) do
    assert(world.SeaWeight(island.X, island.Z) == 0, "Fog over island center")
    assert(world.SeaWeight(island.X, island.DockZ + 45) == 0, "Fog over landing")
end
assert(world.SeaWeight(2300, 0) > 0.99, "Open sea should be mistier")
assert(world.SeaWeight(0, 0) == 0, "Hub should stay clear")
local last = world.SeaWeight(1700, 0)
for x = 1701, 2500 do
    local weight = world.SeaWeight(x, 0)
    assert(weight >= 0 and weight <= 1, "Invalid blend")
    assert(math.abs(weight-last) < 0.01, "Abrupt fog boundary")
    last = weight
end
print("Weather geography: 14 centers, 14 docks, open sea and 800 transition samples passed")
