import bpy

background_image_path = 'background.png'
output_path = '/Users/linyingyou/NTUT/blender/blender'

bpy.context.scene.render.film_transparent = True

# set node tree
bpy.data.scenes["Scene"].use_nodes = True
tree = bpy.context.scene.node_tree
links = tree.links
for node in tree.nodes: 
    tree.nodes.remove(node)

image_node = tree.nodes.new(type='CompositorNodeImage')
image_node.image = bpy.data.images.load(background_image_path)
image_scale_node = tree.nodes.new(type='CompositorNodeScale')
image_scale_node.space = 'RENDER_SIZE'
links.new(image_node.outputs[0], image_scale_node.inputs[0])

render_node = tree.nodes.new(type='CompositorNodeRLayers')
render_scale_node = tree.nodes.new(type='CompositorNodeScale')
render_scale_node.space = 'RENDER_SIZE'
links.new(render_node.outputs[0], render_scale_node.inputs[0])

alpha_over_node = tree.nodes.new(type='CompositorNodeAlphaOver')
links.new(image_scale_node.outputs[0], alpha_over_node.inputs[1])
links.new(render_scale_node.outputs[0], alpha_over_node.inputs[2])

composite_node = tree.nodes.new(type='CompositorNodeComposite')
links.new(alpha_over_node.outputs[0], composite_node.inputs[0])

# render the scene
bpy.data.scenes["Scene"].render.resolution_x = 1920
bpy.data.scenes["Scene"].render.resolution_y = 1080
bpy.data.scenes["Scene"].render.resolution_percentage = 100
bpy.data.scenes["Scene"].render.filepath = 'img/1/blender.png'

bpy.ops.render.render(write_still=True, use_viewport=True)

# 清理Blender場景
for obj in bpy.data.objects:
    obj.select_set(False)
bpy.ops.object.delete(use_global=False)
# 回覆預設場景
bpy.ops.wm.read_factory_settings()