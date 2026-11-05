"""Non-overlapping axis-aligned paving surfaces."""


def rectangle_union(rects):
    levels = sorted({z for _, a, _, b in rects for z in (a, b)})
    result = []
    for low, high in zip(levels, levels[1:]):
        spans = sorted((x0, x1) for x0, z0, x1, z1 in rects if z0 < high and z1 > low)
        merged = []
        for start, end in spans:
            if merged and start <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))
        for start, end in merged:
            prior = next((i for i, (x0,z0,x1,z1) in enumerate(result) if x0 == start and x1 == end and z1 == low), None)
            if prior is None:
                result.append((start, low, end, high))
            else:
                x0,z0,x1,_ = result[prior]
                result[prior] = (x0,z0,x1,high)
    return result
