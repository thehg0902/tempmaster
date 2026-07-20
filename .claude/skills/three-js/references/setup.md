# Scene Setup Skeleton
Init on intersection: create WebGLRenderer({antialias:true, alpha:true}),
scene, camera (35-50 fov), resize handler (debounced, updates aspect +
setSize with capped pixelRatio). Lights: hemisphere + one directional is
enough for most product/logo scenes. Animation loop owns a single clock;
all motion derives from elapsed time (frame-rate independent).
Dispose pattern on teardown: geometry.dispose(), material.dispose(),
renderer.dispose(), cancelAnimationFrame. Keep the module factory-shaped:
initScene(canvas) -> {destroy()}.
