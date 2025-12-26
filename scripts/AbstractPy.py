import bpy
import math

# setup scene
world_obj = bpy.data.worlds["World"]
world_obj.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)

bpy.context.scene.render.engine = "CYCLES"
bpy.context.scene.cycles.device = "GPU"
bpy.context.scene.cycles.samples = 300
bpy.context.scene.render.resolution_y = 1080 * 2
bpy.context.scene.render.resolution_x = 1080 * 2

# delate everything before we start building the scene
# make sure object mode is selected 
if bpy.context.object and bpy.context.object.mode != "OBJECT":
    bpy.ops.object.mode_set(mode="OBJECT")
#delate
for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
bpy.ops.outliner.orphans_purge(do_recursive=True)


# camera setup
bpy.ops.object.camera_add(location=(-11.0, 0.0, 0.0), rotation=(math.radians(90), 0, math.radians(-90)))
camera_object = bpy.context.active_object
camera_object.data.lens = 70
bpy.context.scene.camera = camera_object

# backdrop
bpy.ops.mesh.primitive_plane_add(size=20, location=(5, 0, 0), rotation=(0, math.radians(90), 0))

# light
bpy.ops.object.light_add(type="AREA", location=(0, 0, 5))
bpy.context.object.data.energy = 100

# emitter object
bpy.ops.curve.primitive_bezier_circle_add(radius=1, rotation=(0, math.radians(90), 0))
emitter_object = bpy.context.active_object
emitter_object.data.bevel_depth = 0.01
emitter_object.data.extrude = 0.02
emitter_object.show_instancer_for_render = False # don't show emitter in the render
bpy.ops.object.convert(target="MESH")

# particle system
bpy.ops.object.particle_system_add()
psys_settings = bpy.data.particles["ParticleSettings"]
psys_settings.type = "HAIR"
psys_settings.count = 10000
psys_settings.hair_length = 2
psys_settings.hair_step = 6
psys_settings.display_step = 6
psys_settings.render_step = 6

# create force field 
bpy.ops.object.effector_add(type="TURBULENCE", location=(0, 0, 1.29))
bpy.context.object.field.strength = 23

# material
emission_strength = 20.0
emission_color = (1, 0, 0, 1)
material = bpy.data.materials.new(name = "HairStrandGlowMaterial")
material.use_nodes = True
material_node_tree = material.node_tree

for node in material_node_tree.nodes:
    material_node_tree.nodes.remove(node)
x = 450

current_node_location = 0
hair_info_node = material_node_tree.nodes.new("ShaderNodeHairInfo")
current_node_location += x

color_ramp_node = material_node_tree.nodes.new("ShaderNodeValToRGB")
color_ramp_node.color_ramp.interpolation = "CONSTANT"
color_ramp_node.location.x = current_node_location
current_node_location += x
colorramp_cre_1 = color_ramp_node.color_ramp.elements[1]
colorramp_cre_1.position = 0.98

math_node = material_node_tree.nodes.new("ShaderNodeMath")
math_node.location.x = current_node_location
current_node_location += x
math_node.operation = "MULTIPLY"
math_node.inputs[1].default_value = emission_strength

principled_bsdf_node = material_node_tree.nodes.new("ShaderNodeBsdfPrincipled")
principled_bsdf_node.location.x = current_node_location
current_node_location += x
if emission_color:
    principled_bsdf_node.inputs["Emission Color"].default_value = emission_color
    
material_output_node = material_node_tree.nodes.new("ShaderNodeOutputMaterial")
material_output_node.location.x = current_node_location

# create links between nodes
material_node_tree.links.new(principled_bsdf_node.outputs["BSDF"], material_output_node.inputs["Surface"])
material_node_tree.links.new(hair_info_node.outputs["Random"], color_ramp_node.inputs["Fac"])
material_node_tree.links.new(color_ramp_node.outputs["Color"], math_node.inputs["Value"])
material_node_tree.links.new(math_node.outputs["Value"], principled_bsdf_node.inputs["Emission Strength"])

# apply material to emitter object
emitter_object.data.materials.append(material)

