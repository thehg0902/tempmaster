# 3D Performance Budget
Draw calls < 50; triangles < 150k; texture memory < 32MB; single scene.
Measure: render loop wraps a lightweight FPS meter in dev only; if
sustained <45fps on a throttled run, cut in this order: shadows off ->
pixelRatio 1.5 -> geometry LOD -> drop the scene to poster (yes, really -
a slow scene converts worse than a good image).
Battery: pause on visibilitychange hidden and when canvas < 10% visible.
