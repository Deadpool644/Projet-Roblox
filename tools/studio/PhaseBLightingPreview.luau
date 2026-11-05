-- ModuleScript d'éditeur : aperçu seulement, aucun terrain/décor/collider modifié.
-- Importer dans ServerStorage/ArtTools/PhaseBLightingPreview puis, barre de commandes :
-- require(game.ServerStorage.ArtTools.PhaseBLightingPreview).apply()
-- .restore() remet les valeurs capturées avant le premier apply de cette session.
-- Ne pas l'installer comme Script de jeu. Le contrôleur météo existant reste à unifier.
local Lighting = game:GetService("Lighting")
local RunService = game:GetService("RunService")
local History = game:GetService("ChangeHistoryService")
local Preview = {}
local original = nil

local lightValues = {
    ClockTime = 16.5, Brightness = 2.5, ExposureCompensation = 0.05,
    EnvironmentDiffuseScale = 0.7, EnvironmentSpecularScale = 0.6,
    ShadowSoftness = 0.3, GlobalShadows = true,
    Ambient = Color3.new(0.28, 0.29, 0.33),
    OutdoorAmbient = Color3.new(0.48, 0.47, 0.45),
}
local effects = {
    { Class = "Atmosphere", Name = "HarborAtmosphere", Values = {
        Density = 0.34, Offset = 0.25, Color = Color3.new(0.88, 0.83, 0.76),
        Decay = Color3.new(0.47, 0.51, 0.56), Glare = 0.12, Haze = 1.5,
    } },
    { Class = "BloomEffect", Name = "LanternBloom", Values = {
        Intensity = 0.3, Size = 28, Threshold = 1, Enabled = true,
    } },
    { Class = "ColorCorrectionEffect", Name = "HarborGrade", Values = {
        Contrast = 0.08, Saturation = 0.08, Brightness = 0,
        TintColor = Color3.new(1, 0.98, 0.95), Enabled = true,
    } },
    { Class = "SunRaysEffect", Name = "ArtSunRays", Values = {
        Intensity = 0.05, Spread = 0.7, Enabled = true,
    } },
    { Class = "DepthOfFieldEffect", Name = "ArtDepthOfField", Values = {
        FarIntensity = 0.05, NearIntensity = 0, FocusDistance = 100,
        InFocusRadius = 80, Enabled = true,
    } },
}

local function editorOnly()
    assert(RunService:IsStudio() and not RunService:IsRunning(),
        "Utiliser en édition dans Studio, hors d'une session Jouer.")
end

function Preview.restore()
    editorOnly()
    if not original then return end
    for key, value in pairs(original.Lighting) do Lighting[key] = value end
    for _, entry in ipairs(original.Effects) do
        if entry.Created then
            entry.Instance:Destroy()
        elseif entry.Instance.Parent then
            for key, value in pairs(entry.Values) do entry.Instance[key] = value end
        end
    end
    original = nil
    History:SetWaypoint("Restaurer l'éclairage avant aperçu")
end

function Preview.apply()
    editorOnly()
    -- Preflight before any mutation: never stack a second effect of the same type.
    for _, spec in ipairs(effects) do
        local found = nil
        for _, child in ipairs(Lighting:GetChildren()) do
            if child:IsA(spec.Class) then
                assert(found == nil, "Plusieurs " .. spec.Class .. " : auditer les doublons avant l'aperçu.")
                found = child
            end
        end
    end
    -- Technology is editor-controlled/deprecated on some Studio versions.
    -- Validate the active renderer rather than fail during rollback of a locked property.
    local realistic = false
    pcall(function() realistic = Lighting.LightingStyle == Enum.LightingStyle.Realistic end)
    assert(realistic or Lighting.Technology == Enum.Technology.Future,
        "Sélectionner Realistic/Future dans les propriétés de Lighting avant l'aperçu.")
    if original then Preview.restore() end
    -- Resolve again after restore, which removes effects created by an earlier preview.
    original = { Lighting = {}, Effects = {} }
    History:SetWaypoint("Avant aperçu lumière phase B")
    local ok, message = pcall(function()
        for key, value in pairs(lightValues) do
            original.Lighting[key] = Lighting[key]
            Lighting[key] = value
        end
        for _, spec in ipairs(effects) do
            local target = Lighting:FindFirstChildOfClass(spec.Class)
            local created = target == nil
            if created then
                target = Instance.new(spec.Class)
                target.Name = spec.Name
                target.Parent = Lighting
            end
            local entry = { Instance = target, Created = created, Values = {} }
            table.insert(original.Effects, entry)
            for key, value in pairs(spec.Values) do
                entry.Values[key] = target[key]
                target[key] = value
            end
        end
    end)
    if not ok then
        Preview.restore()
        error("Aperçu annulé et valeurs restaurées : " .. tostring(message))
    end
    History:SetWaypoint("Aperçu lumière phase B")
    warn("Aperçu d'édition uniquement. Sky premium manquant ; MaritimeWeather réécrit l'atmosphère en jeu. Phase B non validée.")
    return { SkyPending = true, RuntimeProfilePending = true, NativeVisualValidationPending = true }
end

return Preview
