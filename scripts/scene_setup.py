import importlib
import sys
import bpy

# auto load script in blender
script_path = r"C:\Users\Pawel\3D Objects\Blender\Python\scripts"
if script_path not in sys.path:
    sys.path.append(script_path)
    
import scene_setup
importlib.reload(scene_setup)

# setup scene
world_obj = bpy.data.worlds["World"]
world_obj.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)

bpy.context.scene.render.engine = "CYCLES"
bpy.context.scene.cycles.device = "GPU"
bpy.context.scene.cycles.samples = 300