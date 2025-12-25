import bpy

# setup scene
world_obj = bpy.data.worlds["World"]
world_obj.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)

bpy.context.scene.render.engine = "CYCLES"
bpy.context.scene.cycles.device = "GPU"
bpy.context.scene.cycles.samples = 300
